def add_attachment_data(response, instance, field_name):
    attachment_field = getattr(instance, field_name, None)
    if attachment_field:
        parts = attachment_field.name.split("/")
        file_name = parts[-1]
        file_type = file_name.split(".")[-1]
        attachment_data = {
            "url": response.pop(field_name),
            "size": attachment_field.size,
            "name": file_name,
            "type": file_type,
        }
        response[field_name] = attachment_data
    return response
