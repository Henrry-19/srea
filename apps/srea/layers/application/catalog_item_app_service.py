from apps.srea.models import CatalogItem


class CatalogoItemAppService(object):

    @staticmethod
    def get_catalogo_item_default(catalog_code, catalog_item_catalog_code):
        return CatalogItem.objects.filter(catalog_code=catalog_code, code=catalog_item_catalog_code, active=True).first()

    @staticmethod
    def get_catalogo_item_lista(catalog_code):
        return CatalogItem.objects.filter(catalog__code=catalog_code, active=True)
