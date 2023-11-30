from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse
import pdfkit 

from .forms import UserRegistrationForm, UserAddressForm


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    
    def get_success_url(self):
        return reverse_lazy('transactions:transaction_report')


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
    

class UserDeleteView(LoginRequiredMixin, RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.request.user.delete()
        return super().get_redirect_url(*args, **kwargs)
    


class DownloadReportView(View):
    def get(self, request, *args, **kwargs):
        # Generate the transaction report data
        report_data = generate_transaction_report_data()  # Replace this with your actual logic to generate the report data

        # Render the transaction report template with the data
        report_html = render_to_string('transactions/transaction_report.html', {'report_data': report_data})

        # Convert the HTML report to PDF using a library like pdfkit, weasyprint, or xhtml2pdf
        pdf_content = convert_html_to_pdf(report_html)  # Replace this with the actual implementation using your preferred library

        # Generate the response as a downloadable file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transaction_report.pdf"'
        response.write(pdf_content)

        # Return the response
        return response

def generate_transaction_report_data():
    # Implement your logic to generate the transaction report data
    # Replace this with your actual implementation
    report_data = {
        'title': 'Transaction Report',
        'transactions': [
            {'id': 1, 'amount': 100},
            {'id': 2, 'amount': 200},
            {'id': 3, 'amount': 300},
        ],
        # Add more data fields as needed
    }
    return report_data

def convert_html_to_pdf(html_content):
    # Implement the conversion from HTML to PDF using your preferred library
    # Replace this with the actual implementation using your preferred library
    pdf_content = '<pdf_content>'
    return pdf_content