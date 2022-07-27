from rest_framework import serializers
from .models import Top, Features, Description, Banners, MobileBanners, Footer











class TopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top
        fields = ('slogan_text', 'buttonText_text')







class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ('title', 'description', 'image')






class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ('title', 'description', 'image', 'button_title', 'button_link')







class BannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = ('image', 'link')








class MobileBannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileBanners
        fields = ('image', 'link')













class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = '__all__' 
        #fields = ('copyright_text', 'slogan_text', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', )









#End
