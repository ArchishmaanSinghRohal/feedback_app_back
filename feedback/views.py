import os
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from feedback.models import Videos, Form_feedback
from feedback.serializers import SnippetSerializer, UserSerializer, FormSerializer
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from feedback.permissions import IsOwnerOrReadOnly

# --- ADD THIS BLOCK TO INITIALIZE FIREBASE ---
# (Place this near the top, after imports)
try:
    cred_path = os.path.join(settings.BASE_DIR, 'firebase-admin-key.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
except ValueError:
    # This try/except block prevents a crash on server reload
    pass 
# --- END OF FIREBASE INIT ---

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Videos.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(uploader_id=self.request.user)

class FormList(mixins.CreateModelMixin, # Keep CreateModelMixin for POST
               generics.GenericAPIView): # Remove ListModelMixin
    # queryset = Form_feedback.objects.all() # We don't need the full queryset here anymore
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, # Allow GET even if not logged in? Or IsAuthenticated?
                          IsOwnerOrReadOnly] # IsOwnerOrReadOnly applies to object-level for PUT/PATCH/DELETE, not needed for list

    # Override the GET method
    def get(self, request, *args, **kwargs):
        # Ensure the user is authenticated to filter by them
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
            
        # Filter the queryset for the current logged-in user
        user_feedback = Form_feedback.objects.filter(filled_by=request.user)
        
        # Serialize the filtered data
        serializer = self.get_serializer(user_feedback, many=True) # Use get_serializer for consistency
        
        # Return the response
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(filled_by=self.request.user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FirebaseTokenView(APIView):
    """
    Creates a Firebase custom token for an authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated] # Uses your IsAuthenticated

    def get(self, request, *args, **kwargs):
        try:
            # Get the user's ID from the Django request
            # This ID will become the 'uid' in Firebase
            user_uid = str(request.user.id) 
            
            # Create a Firebase custom token for this user
            custom_token_bytes = auth.create_custom_token(user_uid)
            
            # Decode to string to send as JSON
            custom_token = custom_token_bytes.decode('utf-8')
            
            return Response(
                {'firebaseToken': custom_token}, 
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Firebase Token Error: {e}")
            return Response(
                {'error': 'Could not generate Firebase token'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )