![Social Preview](https://github.com/mateoniksic/project-storyshare/assets/57192709/0f5a4e79-3016-4dcf-b4b4-777074af96c4)

# What is StoryShare?
StoryShare is a web-based social sharing platform designed to help people connect and share meaningful insights with each other. It's an online web-based application that encourages individuals to spread words of wisdom, lessons learned, and valuable advice to others across the globe.

Whether you're a student, professional, or anyone in between, StoryShare is open to all. You can easily create a free account and start following interesting individuals to see what they have to share. Moreover, you can also contribute your own personal stories and experiences with the community, helping to inspire and motivate others.

Joining StoryShare is a great way to connect with like-minded individuals, share your experiences, and gain valuable insights from others around the world. With a user-friendly interface and a vast network of users, StoryShare is an excellent platform for anyone who values learning and personal growth.

# What was the development process?
1. Created models *(UserProfile, Post, Tags)* with relationships one to one, one to many, many to many.
2. Created factories for models using Faker *(UserFactory, UserProfileFactory, TagFactory, PostFactory)* and generated fake data in bulk using command/script: `python manage.py build_test_data`
3. Used Django Class-Based-Views *(create, list/detail, update, delete)* to process data from models and forms.
4. Used Django Templating Language *(DTL)* to create templates and template components for views using HTML, CSS (BEM), and Javascript.
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
    - Explore stories that are using the same tag name

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
https://github.com/mateoniksic/project-storyshare/assets/57192709/5c31b827-7ddb-4565-81ce-641fe1a1ccb1
