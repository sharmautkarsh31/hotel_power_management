
def generic_save_model_name(model_obj):
    if model_obj.pk is None and (model_obj.name is None or model_obj.name == ''):
        model_obj.name = create_model_name(model_obj)
    return model_obj

def create_model_name(model_obj):
    last_obj = model_obj._meta.model.objects.last()
    if last_obj:
        name = model_obj._meta.model_name + ' ' + str(last_obj.id+1)
    else:
        name = model_obj._meta.model_name + ' 1'
    return name