from django import forms
from .models import ReviewRating

class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model= ReviewRating
        fields=['review','rating']    

#     rating = forms.ChoiceField(
#         choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
#         widget=forms.RadioSelect(attrs={'class': 'star-input'})
#     )    

class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model= ReviewRating
        fields=['review','rating']  