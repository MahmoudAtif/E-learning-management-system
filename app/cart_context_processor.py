from app.models import ShopCart
from user.models import Student



def get_cart(request):
    try:
        # student=Student.objects.get(student=request.user)
        student=request.user.student
        carts=student.student_carts.all()
        total_carts=student.student_carts.all().count()
        total_price=0
        for item in carts:
            total_price+=item.price
        return {
            'carts':carts,
            'total_carts':total_carts,
            'total_price':total_price,
        }
    except:
        return {
            
        }
