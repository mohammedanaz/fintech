from django.contrib.auth.models import  BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:  
            user.set_password(password)
        else:  
            raise ValueError('The Password field must be set')
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, and password.
        """
        extra_fields.setdefault('role', 'admin')
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True  
        user.is_staff = True  
        user.save(using=self._db)
        return user