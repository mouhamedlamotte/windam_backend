from rest_framework import serializers
from .models import User



class UserAccountSerializer(serializers.ModelSerializer):
    
    
    class Meta :
        model = User
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_email_verified',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_email_verified' : {'read_only' : True},
            'is_active' : {'read_only' : True},
            'is_staff' : {'read_only' : True},
            'is_superuser' : {'read_only' : True},
            'date_joined' : {'read_only' : True},
            }
        
    
        
        
    def create(self, validated_data):
        # validated_data['is_active'] = False
        user = User(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
class UpdateUserAccountSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = [
            'first_name',
            'last_name',
            # 'birth_date',
            'is_email_verified',
        ]
        extra_kwargs = {
            'is_email_verified' : {'write_only' : True},
            }
        

class UserAccountPubliqueSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
        ]