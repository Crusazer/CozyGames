from celery import shared_task
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.apps import apps

logger = logging.getLogger(__name__)


@shared_task()
def create_thumbnail_image(model_name, instance_id: int, size: tuple):
    try:
        Model = apps.get_model('forum', model_name)
        instance = Model.objects.get(id=instance_id)
        if instance.image:
            image_path = instance.image.path
            thumbnail_path = 'media/thumbnails/' + instance.image.name.split('/')[-1]

            image = Image.open(image_path)

            image.thumbnail(size)
            with open(thumbnail_path, 'wb') as thumbnail_file:
                image = image.convert('RGB')
                image.save(thumbnail_file, 'JPEG')

            logger.info(f"Thumbnail for {model_name} with id {instance_id} created successfully.")
            return {
                'status': 'success',
                'message': f"Thumbnail for {model_name} with id {instance_id} created successfully.",
                'thumbnail_path': thumbnail_path
            }
        else:
            logger.error(f"{model_name} with id {instance_id} does not have an image.")
            return {
                'status': 'error',
                'message': f"{model_name} with id {instance_id} does not have an image.",
                'thumbnail_path': None
            }
    except ObjectDoesNotExist:
        logger.error(f"{model_name} with id {instance_id} does not exist.")
        return {
            'status': 'error',
            'message': f"{model_name} with id {instance_id} does not exist.",
            'thumbnail_path': None
        }
    except Exception as e:
        logger.error(f"Error creating thumbnail for {model_name} with id {instance_id}: {e}")
        return {
            'status': 'error',
            'message': f"Error: {e}",
            'thumbnail_path': None
        }
