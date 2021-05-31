
def generic_save_model_name(model_obj, name=None):
    if model_obj.pk is None and (model_obj.name is None or model_obj.name == ''):
        if name:
            model_obj.name = create_model_name(model_obj, name)
        else:
            model_obj.name = create_model_name(model_obj)
    return model_obj

def create_model_name(model_obj, name=None):
    last_obj = model_obj._meta.model.objects.last()
    if not name:
        name = model_obj._meta.model_name
    if last_obj:
        final_name = name + ' ' + str(last_obj.id+1)
    else:
        final_name = name + ' 1'
    return final_name