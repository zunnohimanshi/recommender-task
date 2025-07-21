from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubmissionSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# ✅ This is your main API view that Streamlit is calling
@method_decorator(csrf_exempt, name='dispatch')
class SubmitDataView(APIView):
    def post(self, request):
        data = request.data.get('data')  # Expecting {"data": {...}} in request body
        if not data:
            return Response({"error": "Missing 'data' field"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
