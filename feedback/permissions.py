from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the user linked by 'uploader_id' 
    or 'filled_by' to edit the object.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the object has an 'uploader_id' attribute (for Videos)
        if hasattr(obj, 'uploader_id'):
            return obj.uploader_id == request.user
            
        # Check if the object has a 'filled_by' attribute (for Form_feedback)
        if hasattr(obj, 'filled_by'):
            return obj.filled_by == request.user
            
        # Default to False if the field isn't found
        return False