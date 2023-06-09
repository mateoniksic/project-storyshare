![Social Preview](https://github.com/mateoniksic/project-storyshare/assets/57192709/0f5a4e79-3016-4dcf-b4b4-777074af96c4)

# What is StoryShare?
StoryShare is a web-based social sharing platform designed to help people connect and share meaningful insights with each other. It's an online web-based application that encourages individuals to spread words of wisdom, lessons learned, and valuable advice to others across the globe.

Whether you're a student, professional, or anyone in between, StoryShare is open to all. You can easily create a free account and start following interesting individuals to see what they have to share. Moreover, you can also contribute your own personal stories and experiences with the community, helping to inspire and motivate others.

Joining StoryShare is a great way to connect with like-minded individuals, share your experiences, and gain valuable insights from others around the world. With a user-friendly interface and a vast network of users, StoryShare is an excellent platform for anyone who values learning and personal growth.

# What was the development process?
1. Created models *(UserProfile, Post, Tags)* with relationships one to one, one to many, many to many.
2. Created factories for models using Faker *(UserFactory, UserProfileFactory, TagFactory, PostFactory)* and generated fake data in bulk using command/script: `python manage.py build_test_data`
3. Used Django Class-Based-Views *(create, list/detail, update, delete)* to process data from models and forms.
4. Used Django Templating Language *(DTL)* to create templates and template components for views using HTML, CSS (BEM) and Javascript.
5. Wrote 51 unit test(s) for urls, models and views.

# What are the core features?

- **User account**
    - Account creation *(sign up, sign in, sign out)*
    - Account update *(username, first name, last name, email)*
- **User profile**
    - Profile update *(profile image, description)*
- **Stories**
    - Create a new story *(title, content, summary, featured image, tags)*
    - Update or delete existing stories
- **Search**
    - Search users by username
- **Pages**
    - For you *(shows stories from users you don’t follow)*
    - Following *(shows stories from users you follow)*
- **Other**
    - Follow or unfollow users
    - Explore stories which are using the same tag name

# What is the tech stack?

- Python *(3.11.0.)* / Django *(4.1.3.)*
- HTML / CSS
- Javascript

# How to start the application?

1. **Clone repository**
2. **Run command:** `python manage.py runserver`
3. **Open in browser:** http://127.0.0.1:8000/
4. **Stop command:** CTRL + C

# Live preview
- [[ CLICK HERE TO EXPERIENCE STORYSHARE IN ACTION → ]](https://mateoniksic.pythonanywhere.com/)

# Sneak peek
![home](https://user-images.githubusercontent.com/57192709/226345535-bdb520bd-3841-4100-b867-77bcad73158a.png)
![signin](https://user-images.githubusercontent.com/57192709/226345542-4277448e-5f1a-43e9-a6b2-d81fd25b5370.png)
![signup](https://user-images.githubusercontent.com/57192709/226345552-94d40a09-067a-4e28-9085-f26899d7c0a4.png)
![for-you](https://user-images.githubusercontent.com/57192709/226345567-c33e751c-832d-453e-8a0f-5271a8a51826.png)
![following](https://user-images.githubusercontent.com/57192709/226345576-b6e6bb04-a011-41fd-a9b4-76f86e7dc0f3.PNG)
![search mat](https://user-images.githubusercontent.com/57192709/226345614-4cdd9cdb-d75f-4f03-99cf-0941fd2ac124.PNG)
![search](https://user-images.githubusercontent.com/57192709/226345664-598bb279-8b00-491c-934f-856b6b1b86e6.PNG)
![create](https://user-images.githubusercontent.com/57192709/226345690-c1a7f72f-a24b-4639-a511-573e5d49c95f.PNG)
![profile](https://user-images.githubusercontent.com/57192709/226345708-a554d589-6be0-4917-9caf-45fa811a9432.PNG)
![profile edit](https://user-images.githubusercontent.com/57192709/226345726-2a370709-539c-4f48-ad7d-887c6c51612a.PNG)
![profile followers](https://user-images.githubusercontent.com/57192709/226345736-63e4f32b-8b1c-4cff-b5fe-bd707d599601.PNG)
![settings](https://user-images.githubusercontent.com/57192709/226345753-1ba02ff7-112f-422c-82f7-9d563f31d017.PNG)

