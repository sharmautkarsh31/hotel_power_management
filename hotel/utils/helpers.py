
def generic_save_model_name(model_obj, name=None):
    if model_obj.pk is None and (model_obj.name is None or model_obj.name == ''):
        if name:
            model_obj.name = create_model_name(model_obj, name)
        else:
            model_obj.name = create_model_name(model_obj)
    return model_obj

def create_model_name(model_obj, name=None):
    obj_count = model_obj._meta.model.objects.count()
    if not name:
        name = model_obj._meta.model_name
    final_name = name + ' ' + str(obj_count+1)
    return final_name