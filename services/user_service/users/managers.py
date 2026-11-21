from django.contrib.auth.models import UserManager as BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Phone number is required.")

        user = self.model(phone=phone)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        if not phone:
            raise ValueError("Error Phone")
        if not password:
            raise ValueError("Superuser must have password")

        user = self.model(phone=phone)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
