# from django.views.generic import TemplateView
#
# from hotel.models import Hotel
# from hotel.serializers import HotelApplianceSerializer
#
#
# class Home(TemplateView):
#     template_name = 'list_hotels.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         hotel_list = Hotel.objects.all().values('id','name')
#         context['hotels'] =hotel_list
#         return context
#
#
# class Dashboard(TemplateView):
#     template_name = 'dashboard.html'
#
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         object = Hotel.objects.filter(id=kwargs['id']).first()
#         context['hotel_artefacts'] = HotelApplianceSerializer(object).data
#         return context
#
#     # def get(self, request, *args, **kwargs):
#     #     context = self.get_context_data(**kwargs)
#     #     return self.render_to_response(context)
#
