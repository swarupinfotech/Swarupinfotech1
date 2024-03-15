from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout as auth_logout
# Create your views here.


def home(request):
	home = Home.objects.all()
	cate = Category.objects.all()

	allPost = Post.objects.all()
	RecentPost = Post.objects.all()[::-1]

	data = request.GET.get('category')
	if data is not None:
		cate_data = Post.objects.filter(category=data)
		context = {'home':home,'cate_filter':cate_data,'cate':cate}
		return render(request,'blog/category.html',context)


	context = {'home':home,'cate':cate,'posts':allPost,'recentpost':RecentPost}
	return render(request,'blog/index.html',context)


def blog(request):
	home = Home.objects.all()
	cate = Category.objects.all()
	allPost = Post.objects.all()[::-1]



	context = {'home':home,'cate':cate,'posts':allPost}
	return render(request,'blog/blog.html',context)

def contact(request):
	home = Home.objects.all()
	cate = Category.objects.all()

	context = {'home':home,'cate':cate}

	if request.method == "POST":
		firstname = request.POST['fname']
		lastname = request.POST['lname']
		email  = request.POST['email']
		subject = request.POST['subject']
		message = request.POST['message']

		if len(firstname) > 4:
			contact = Contact(first_name=firstname,last_name=lastname,email=email,subject=subject,message=message)
			contact.save()
			messages.success(request,'Successfully Form Submit')
			return redirect('/contact')
		else:
			messages.error(request,'First Name Should Be more then 4 chars')
			return redirect('/contact')


	return render(request,'blog/contact.html',context)


def category(request):
	home = Home.objects.all()
	cate = Category.objects.all()

	context = {'home':home,'cate':cate}
	return render(request,'blog/category.html',context)

def single(request,slug):
	home = Home.objects.all()
	cate = Category.objects.all()
	post = Post.objects.filter(slug=slug).first()

	comment = Comment.objects.filter(post=post)
	

	if request.method == "POST":
		name = request.POST['name']
		email = request.POST['email']
		postsno = request.POST.get('postsno')
		website = request.POST['website']
		message = request.POST['message']

		post_data = Post.objects.get(sno=postsno)
		
		comment = Comment(name=name,email=email,post=post_data,website=website,message=message)
		comment.save()
		messages.success(request,"Comment Successfully Submit")

		return redirect('/')


	context = {'home':home,'cate':cate,'post':post,'comment':comment}
	return render(request,'blog/single.html',context)


	


def login(request):
	if request.user.is_authenticated:
		return  redirect('/')

	if request.method == 'POST':
		number = request.POST['number']
		password = request.POST['password']

		print(password)

		user = authenticate(request,username=number,password=password)
		print(user)
		if user is not None:
			auth_login(request,user)
			messages.success(request,"Successfully Login")
			return redirect('/')
		else:
			messages.error(request,"Something Went Wrong")
			return redirect('/login')
	return render(request,'auth/login.html')

def signup(request):
	if request.user.is_authenticated:
		return  redirect('/')

	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		number = request.POST['number']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']

		
		number_check = User.objects.filter(username=number).exists()
		email_check = User.objects.filter(email=email).exists()
		
		if number_check == True:
			messages.error(request,"Your Number  Already Exists")
			return redirect('/signup')
		
		if email_check == True:
			messages.error(request,"Your Email Already Exists")
			return redirect('/signup')


		if len(number) != 10:
			messages.error(request,'Number Should Be 10 Digit')
			return redirect('/signup')
		
		elif password != cpassword:
			messages.error(request,"Password And Confirm Did'nt Match")
			return redirect('/signup')

		else:
			user = User.objects.create_user(username=number,email=email,password=cpassword)
			user.first_name = fname 
			user.last_name = lname 
			user.save()
			messages.success(request,"Your Account Successfully Created")
			return redirect('/login')


	return render(request,'auth/signup.html')


def logout(request):
	auth_logout(request)
	messages.success(request,"Logout Succesfully")
	return redirect('/')