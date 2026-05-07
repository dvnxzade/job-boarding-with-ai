from .serializers import ApplicationSerializer , JobSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Job , Application
from rest_framework import status

# Create your views here.

class ApplyToJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , id):
        cover_letter = request.data.get("cover_letter")
        cv = request.FILES.get("cv")

        if not cover_letter or not cv:
            return Response({
                "message" : "All fields are required",
            } , status = status.HTTP_400_BAD_REQUEST)

        try :
            job = Job.objects.get(pk=id)
        except:
            return Response(
                {
                    "message": "Job doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        # build auth
        user = request.user
        if user.status != "applicant":
            return Response({
                "message" : "Employers can't apply for jobs!",
                
            },status=status.HTTP_403_FORBIDDEN)

        data = {
            "job" : job.id,
            "applicant" : user.id,
            "cover_letter" : cover_letter,
            "cv" : cv
        }

        # call seralizer
        serializer = ApplicationSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        new_application = serializer.save()

        return Response({
            "message" : 'Application sent successfully!',
            "id" : new_application.id
        }, status = status.HTTP_201_CREATED)


class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer