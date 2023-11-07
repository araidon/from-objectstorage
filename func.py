import io
import json
import logging
import oci

from fdk import response

def handler(ctx, data: io.BytesIO = None):
    name = "World"
    try:
        body = json.loads(data.getvalue())
        name = body.get("name")
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))
    
    FILENAME = json.dumps(body.get("data").get("resourceName"))
    BUCKET_NAME = json.dumps(body.get("data").get("additionalDetails").get("bucketName"))
    NAMESPACE = json.dumps(body.get("data").get("additionalDetails").get("namespace"))

    # logging.getLogger().info(f"FILENAME={FILENAME}, BUCKET_NAME={BUCKET_NAME}, NAMESPACE={NAMESPACE}")
    print(f"FILENAME={FILENAME}, BUCKET_NAME={BUCKET_NAME}, NAMESPACE={NAMESPACE}")

    signer = oci.auth.signers.get_resource_principals_signer()
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    #object_storage = oci.object_storage.ObjectStorageClient(config)

    #object = object_storage.get_object(NAMESPACE,BUCKET_NAME,FILENAME)
    object = object_storage.list_objects(NAMESPACE,BUCKET_NAME)

    objects = [b.name for b in object.data.objects]

    logging.getLogger().info(objects)

    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )
