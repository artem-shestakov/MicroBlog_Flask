from webapp import celery


@celery.task(bind=True)
def log(self, msg):
    try:
        return msg
    except Exception as e:
        self.retry(exc=e)
