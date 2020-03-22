from haystack import indexes
from .models import For_the_category

class For_the_categoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return For_the_category

    def index_queryset(self, using=None):
    #get_model中哪些数据进入es
        return self.get_model().objects.filter(is_launched=True)

