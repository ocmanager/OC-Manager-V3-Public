from django.views.generic import FormView, View
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .forms import *
from .models import *
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
import json
from finecontrol.calculations.DevCalc import calculateDevelopment
from finecontrol.forms import data_validations, data_validations_and_save, Method_Form
from finecontrol.models import Method_Db
from django.core.exceptions import ObjectDoesNotExist


class DevelopmentDelete(View):

    def delete(self, request, id):
        apps = Development_Db.objects.filter(method=Method_Db.objects.get(pk=id))
        apps.delete()
        return JsonResponse({})

class DevelopmentView(FormView):
    def get(self, request):
        """Manage the HTML view in Development"""
        return render(request, 'development.html', {})


class DevelopmentDetail(View):
    def delete(self, request, id):
        Method_Db.objects.get(pk=id).delete()
        return JsonResponse({})

    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        response = {}
        method = Method_Db.objects.get(pk=id_object)

        if not Development_Db.objects.filter(method=method):
            response.update({"filename": getattr(method, "filename")})
            response.update({"id": id_object})
        else:

            dev_config = Development_Db.objects.get(method=method)
            response.update(model_to_dict(dev_config.pressure_settings.get(), exclude=["id", ]))
            response.update(model_to_dict(dev_config.plate_properties.get(), exclude=["id", ]))
            response.update(model_to_dict(dev_config.band_settings.get(), exclude=["id", ]))
            response.update(model_to_dict(dev_config.zero_properties.get(), exclude=["id", ]))
            response.update(model_to_dict(method))

            flowrate_entry = Flowrate_Db.objects.filter(development=dev_config.id).values('value')
            response.update({'flowrate': [entry for entry in flowrate_entry]})

        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        id = request.POST.get("selected-element-id")
        flowrate = request.POST.get('flowrate')
        flowrate = json.loads(flowrate)

        if not id or not Development_Db.objects.filter(method=Method_Db.objects.get(pk=id)):
            development_form = Development_Form(request.POST)
            if development_form.is_valid():
                development_instance = development_form.save(commit=False)
                development_instance.auth = request.user
                method_form = Method_Form(request.POST)

                if not id:
                    method = method_form.save(commit=False)
                    method.auth = request.user
                    method.save()
                else:
                    method = Method_Db.objects.get(pk=id)
                development_instance.method = method
                development_instance.save()
                objects_save = data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST),
                    pressure_settings=PressureSettings_Form(request.POST),
                    zero_position=ZeroPosition_Form(request.POST),
                    band_settings=DevelopmentBandSettings_Form(request.POST),
                )
                development_instance.pressure_settings.add(objects_save["pressure_settings"])
                development_instance.plate_properties.add(objects_save["plate_properties"])
                development_instance.zero_properties.add(objects_save["zero_position"])
                development_instance.band_settings.add(objects_save["band_settings"])
            else:
                return HttpResponseBadRequest({"error", "Please check all the inputs!"})

        else:
            method = Method_Db.objects.get(pk=id)
            method_form = Method_Form(request.POST, instance=method)
            method_form.save()
            development_instance = Development_Db.objects.get(method=method)
            development_form = Development_Form(request.POST, instance=development_instance)
            dev_inst = development_form.save(commit=False)
            dev_inst.method = method
            dev_inst.save()
            data_validations_and_save(
                plate_properties=PlateProperties_Form(request.POST,
                                                      instance=development_instance.plate_properties.get()),
                pressure_settings=PressureSettings_Form(request.POST,
                                                        instance=development_instance.pressure_settings.get()),
                zero_position=ZeroPosition_Form(request.POST,
                                                instance=development_instance.zero_properties.get()),
                band_settings=DevelopmentBandSettings_Form(request.POST,
                                                           instance=development_instance.band_settings.get()),
            )
            development_instance.flowrates.all().delete()

        for flow_value in flowrate:
            flowrate_form = Flowrate_Form(flow_value)
            if flowrate_form.is_valid():
                flowrate_object = flowrate_form.save()
                development_instance.flowrates.add(flowrate_object)

        return JsonResponse({'message': 'Data !!'})


class DevelopmentAppPlay(View):
    def post(self, request):
        method_id = request.POST.get('selected-element-id')
        development_object = Development_Db.objects.get(method=method_id)
        waiting_times = WaitTime_Db.objects.filter(development=development_object).values('waitTime', 'application')
        flowrates = json.loads(request.POST.get('flowrate'))
        forms_data = data_validations(plate_properties=PlateProperties_Form(request.POST),
                                      pressure_settings=PressureSettings_Form(request.POST),
                                      zero_position=ZeroPosition_Form(request.POST),
                                      band_settings=DevelopmentBandSettings_Form(request.POST))

        forms_data['flowrate'] = flowrates
        forms_data['waiting_times'] = waiting_times
        gcode = calculateDevelopment(forms_data)
        OC_LAB.print_from_list(gcode)
        return JsonResponse({'error': 'f.errors'})


class DevelopmentWaitingTime(View):

    def get(self, request, id):

        query = WaitTime_Db.objects.filter(development=Development_Db.objects.get(method=id)).values('waitTime',
                                                                                                 'application')
        response = list(query)
        if not response:
            return HttpResponseBadRequest({"data": "No Waiting times saved!"})
        else:
            return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.POST['data'])
        dev_id = data['development_id']
      #  print(dev_id)
        try:
            development_object = Development_Db.objects.get(method=dev_id)
            print("Development Object"+str(development_object))
            old_waitingtime = WaitTime_Db.objects.filter(development=development_object)
#            print("oldWaitingTIME Object"+str(old_waitingtime))
            if old_waitingtime:
                old_waitingtime.delete()
 #               print("oldWaitingTIME Object"+str(old_waitingtime))
            for application in data.get('waitingTimes'):
                    obj = WaitTime_Db(development=development_object,
                                      waitTime=application.get('waitingTime'),
                                      application=application.get('application'))
                    obj.save()
            return JsonResponse({"data": f"Data Saved in development_object {dev_id}"})
        except ObjectDoesNotExist:
            return HttpResponseBadRequest({"data": "Development id not Found"})


class DevelopmentViewWaitingTimes(View):

    def get(self, request):
        return render(request, 'modules/development/waitingtime/table/table.html', {})
