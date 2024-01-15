from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CustomUser,Package,Comments,Blogs
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class=CustomUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully",'data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({"message": "User registration failed", "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SuperuserRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            # Set is_superuser to True for superuser registration
            serializer.validated_data['is_superuser'] = True
            serializer.save()
            return Response({"message": "User registered successfully", 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({"message": "User registration failed", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)




class PackageCRUDView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PackageSerializer
    def post(self, request):
        serializer = PackageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['admin'] = self.request.user
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        package = Package.objects.get(pk=pk)
        serializer = PackageSerializer(package, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        package = Package.objects.get(pk=pk)
        serializer = PackageSerializer(package, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            package.delete()
            return Response({'detail': 'Package deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)



class ListPackagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            packages = Package.objects.all()
            serializer = PackageSerializer(packages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Packages not found.'}, status=status.HTTP_404_NOT_FOUND)

class PackageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            serializer = PackageSerializer(package)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            serializer = CommentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.validated_data['user'] = self.request.user
                serializer.validated_data['package'] = package
                serializer.save()
                return Response({"message": "Comment created successfully",'data':serializer.data}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)

class ListCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            comments = Comments.objects.filter(package=package)
            serializer = CommentlistSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            comment = Comments.objects.get(pk=pk, user=request.user)
            comment.delete()
            return Response({'detail': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

        except Comments.DoesNotExist:
            return Response({'detail': 'Comment not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)



class CreateBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBlogsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            blogs = Blogs.objects.all()
            serializer = BloglistSerializer(blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'Blogs not found.'}, status=status.HTTP_404_NOT_FOUND)

class BlogDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk)
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)



class ListUserBlogsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_blogs = Blogs.objects.filter(user=request.user)
            serializer = BloglistSerializer(user_blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'Blogs not found.'}, status=status.HTTP_404_NOT_FOUND)


class UpdateBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk, user=self.request.user)
            serializer = BlogSerializer(blog, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found or you do not have permission to update it.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk, user=self.request.user)
            serializer = BlogSerializer(blog, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found or you do not have permission to update it.'}, status=status.HTTP_404_NOT_FOUND)


class DeleteBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk, user=self.request.user)
            blog.delete()
            return Response({'detail': 'Blog deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)