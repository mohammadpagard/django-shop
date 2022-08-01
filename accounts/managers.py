from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        elif not phone_number:
            raise ValueError('Users must have an phone number')

        elif not full_name:
            raise ValueError('Users must have an full name')
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password=None):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user