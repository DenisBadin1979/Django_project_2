from rest_framework import serializers
from .models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'city', 'avatar')
        read_only_fields = ('id',)


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    user_email = serializers.CharField(source='user.email', read_only=True)
    paid_course_title = serializers.CharField(source='paid_course.title', read_only=True)
    paid_lesson_title = serializers.CharField(source='paid_lesson.title', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'user_email', 'payment_date', 'paid_course',
            'paid_course_title', 'paid_lesson', 'paid_lesson_title',
            'amount', 'payment_method', 'payment_method_display'
        )
        read_only_fields = ('id', 'payment_date', 'user_email', 'paid_course_title',
                            'paid_lesson_title', 'payment_method_display')

    def validate(self, data):
        """Проверка, что указан либо курс, либо урок, но не оба одновременно"""
        paid_course = data.get('paid_course')
        paid_lesson = data.get('paid_lesson')

        if not paid_course and not paid_lesson:
            raise serializers.ValidationError(
                "Необходимо указать либо оплаченный курс, либо оплаченный урок"
            )

        if paid_course and paid_lesson:
            raise serializers.ValidationError(
                "Можно указать только один объект оплаты: курс ИЛИ урок"
            )

        return data


class PaymentDetailSerializer(PaymentSerializer):
    """Детальный сериализатор для платежей с полной информацией"""

    class Meta(PaymentSerializer.Meta):
        fields = PaymentSerializer.Meta.fields + ('payment_date',)


class UserDetailSerializer(UserSerializer):
    """Детальный сериализатор для пользователя с его платежами"""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('payments', 'date_joined', 'last_login')