from django import forms
from .models import Order
from accounts.models import User
import logging

logger = logging.getLogger(__name__)

class CheckoutForm(forms.ModelForm):
    """Form for collecting shipping and payment information."""
    SAME_AS_SHIPPING = 'same'
    DIFFERENT_BILLING = 'different'
    
    BILLING_CHOICES = [
        (SAME_AS_SHIPPING, 'Same as shipping address'),
        (DIFFERENT_BILLING, 'Use a different billing address'),
    ]
    
    billing_option = forms.ChoiceField(
        choices=BILLING_CHOICES,
        widget=forms.RadioSelect,
        initial=SAME_AS_SHIPPING
    )
    
    save_shipping = forms.BooleanField(
        required=False,
        initial=True,
        label='Save shipping address to my profile'
    )
    
    save_billing = forms.BooleanField(
        required=False,
        initial=True,
        label='Save billing address to my profile'
    )
    
    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'billing_address',
            'payment_method',
            'notes'
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 4}),
            'billing_address': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.address:
            self.fields['shipping_address'].initial = self.user.address
        
        self.fields['billing_address'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        billing_option = cleaned_data.get('billing_option')
        
        if billing_option == self.DIFFERENT_BILLING and not cleaned_data.get('billing_address'):
            self.add_error('billing_address', 'Please enter billing address')

        # Validación adicional
        if not cleaned_data.get('shipping_address'):
            raise forms.ValidationError("Por favor ingresa una dirección de envío")
            
        if cleaned_data.get('billing_option') == self.DIFFERENT_BILLING and not cleaned_data.get('billing_address'):
            raise forms.ValidationError("Por favor ingresa una dirección de facturación")
            
        return cleaned_data


    
    def save(self, commit=True):
        order = super().save(commit=False)
        
        if self.user:
            if self.cleaned_data.get('save_shipping'):
                self.user.address = self.cleaned_data['shipping_address']
                self.user.save()
                logger.info(f"Saved shipping address for user {self.user.username}")
            
            if (self.cleaned_data.get('save_billing') and 
                self.cleaned_data.get('billing_address')):
                self.user.billing_address = self.cleaned_data['billing_address']
                self.user.save()
                logger.info(f"Saved billing address for user {self.user.username}")
        
        if commit:
            order.save()
        
        return order