from django.db import models
import uuid

from schools.models import School
from student_parents.models import Child

# Create your models here.
class Application(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    viewed = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    application_id = models.CharField(max_length=11)

    def save(self, *args, **kwargs):
        self.application_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.child.first_name} {self.child.last_name}"

    def student_name(self):
        return f"{self.child.first_name} {self.child.last_name}"
