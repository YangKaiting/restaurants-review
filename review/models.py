from django.db import models
from django.contrib.auth.models import User

# Create User
# u1 = User.objects.create_user(username, email=None, password=None, **extra_fields)
# u1.save()

# Create your models here.

# 1
class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    id = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.id

#2
class Restaurant(models.Model):
    # access child: one restaurant has many rates (restaurant.rate_set.get(user=current_user))

    id = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=50)

    # many restaurants to one category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id


# 3
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    rate = models.IntegerField(default=0)
    description = models.CharField(max_length=255)


# 4
class LikeForReview(models.Model):
    # similar to composite primary key
    class Meta:
        verbose_name_plural = "Like For Reviews"
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# 5
# Note: one user can leave comment on one review many times
class Comment(models.Model):
    # many comments to one review
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    # many comments to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.CharField(max_length=255)


# 6
class LikeForComment(models.Model):
    # similar to composite primary key
    class Meta:
        verbose_name_plural = "Like For Comments"
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)