from django.views import View
from organizations.models import Organization, OrganizationMember
from django.http import Http404


class OrganizationsMixin(View):
    def dispatch(self, request, *args, **kwargs):
        org_code = kwargs["organization_code"]
        try:
            self.organization = Organization.objects.get(code=org_code)
            self.organizationmember = OrganizationMember.objects.filter(
                user=request.user, organization=self.organization
            )
        except Organization.DoesNotExist:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)