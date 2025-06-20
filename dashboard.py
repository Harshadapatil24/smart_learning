from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import os
import random
import json
from datetime import datetime

# Sample data for demonstration
teachers = {
    'math': {'name': 'Dr. Sarah Williams', 'profile_pic': 'math_teacher.jpg', 'bio': 'PhD in Mathematics with 10 years of teaching experience. Specializes in algebra and calculus.'},
    'science': {'name': 'Prof. James Chen', 'profile_pic': 'science_teacher.jpg', 'bio': 'Former research scientist with expertise in physics and chemistry. Passionate about making science accessible.'},
    'programming': {'name': 'Dr. Michael Rodriguez', 'profile_pic': 'programming_teacher.jpg', 'bio': 'Software engineer turned educator. Expert in Python, JavaScript, and web development.'},
    'language': {'name': 'Dr. Emily Thompson', 'profile_pic': 'language_teacher.jpg', 'bio': 'Published author with a doctorate in English Literature. Specializes in creative writing and grammar.'},
    'web': {
        'name': 'Dr. David Wilson',
        'profile_pic': 'web_teacher.jpg',
        'bio': 'Full-stack developer with 12 years of experience. Expert in modern web technologies and frameworks.'
    },
    'mobile': {
        'name': 'Dr. Lisa Zhang',
        'profile_pic': 'mobile_teacher.jpg',
        'bio': 'Mobile development expert with experience in iOS, Android, and cross-platform frameworks.'
    },
    'ai': {
        'name': 'Dr. James Foster',
        'profile_pic': 'ai_teacher.jpg',
        'bio': 'AI researcher and practitioner with expertise in machine learning and deep learning.'
    },
    'cloud': {
        'name': 'Prof. Maria Garcia',
        'profile_pic': 'cloud_teacher.jpg',
        'bio': 'Cloud architect with extensive experience in AWS, Azure, and cloud infrastructure design.'
    },
    'cybersecurity': {
        'name': 'Dr. Robert Chen',
        'profile_pic': 'security_teacher.jpg',
        'bio': 'Cybersecurity expert with background in network security and ethical hacking.'
    },
    'data': {
        'name': 'Dr. Anna Smith',
        'profile_pic': 'data_teacher.jpg',
        'bio': 'Data scientist with expertise in statistical analysis, machine learning, and big data technologies.'
    },
    'blockchain': {
        'name': 'Prof. Michael Lee',
        'profile_pic': 'blockchain_teacher.jpg',
        'bio': 'Blockchain developer and researcher specializing in distributed systems and smart contracts.'
    },
    'game': {
        'name': 'Prof. Sarah Anderson',
        'profile_pic': 'game_teacher.jpg',
        'bio': 'Game developer with experience in Unity, Unreal Engine, and game design principles.'
    }
}

# Subject content data
subject_content = {
    'math': {
        'welcome_message': "Welcome to Mathematics! I'm your AI tutor. I can help with algebra, calculus, statistics, and more. What would you like to learn today?",
        'videos': [
            {
                'title': 'Introduction to Algebra',
                'description': 'Learn the basics of algebraic expressions and equations',
                'youtube_id': 'NybHckSEQBI',
                'duration': '10:15'
            },
            {
                'title': 'Understanding Calculus',
                'description': 'Introduction to derivatives and integrals',
                'youtube_id': '8RqP6Uz_6e4',
                'duration': '15:30'
            }
        ]
    },
    'science': {
        'welcome_message': "Welcome to Science! I'm your AI tutor. I can help with physics, chemistry, biology, and more. What would you like to explore today?",
        'videos': [
            {
                'title': 'Newton\'s Laws of Motion',
                'description': 'Understanding the fundamental laws of physics',
                'youtube_id': 'mn34mnnDnKU',
                'duration': '12:20'
            },
            {
                'title': 'Introduction to Chemistry',
                'description': 'Basic concepts of atoms and molecules',
                'youtube_id': '6pUzPh_lCO8',
                'duration': '14:45'
            }
        ]
    },
    'programming': {
        'welcome_message': "Welcome to Programming! I'm your AI tutor. I can help with Python, JavaScript, data structures, algorithms, and more. What would you like to code today?",
        'videos': [
            {
                'title': 'Python for Beginners',
                'description': 'Getting started with Python programming',
                'youtube_id': 'kqtD5dpn9C8',
                'duration': '13:25'
            },
            {
                'title': 'JavaScript Fundamentals',
                'description': 'Learn the basics of JavaScript',
                'youtube_id': 'W6NZfCO5SIk',
                'duration': '11:50'
            }
        ]
    },
    'language': {
        'welcome_message': "Welcome to Language Arts! I'm your AI tutor. I can help with writing, grammar, literature analysis, and more. What would you like to work on today?",
        'videos': [
            {
                'title': 'Essay Writing Tips',
                'description': 'Learn how to write effective essays',
                'youtube_id': 'IN6IOSMviS4',
                'duration': '16:40'
            },
            {
                'title': 'Grammar Essentials',
                'description': 'Master the basics of English grammar',
                'youtube_id': 'fSrTyw8Fh6Q',
                'duration': '09:55'
            }
        ]
    },
    'web': {
        'welcome_message': "Welcome to Web Development! I'm your AI tutor. I can help with HTML, CSS, JavaScript, frameworks, and more. What would you like to learn today?",
        'videos': [
            {
                'title': 'HTML & CSS Full Course - Beginner to Pro',
                'description': 'Complete web development fundamentals course',
                'youtube_id': 'G3e-cpL7ofc',
                'duration': '6:30:33'
            },
            {
                'title': 'JavaScript Full Course for Beginners',
                'description': 'Complete JavaScript programming course',
                'youtube_id': 'PkZNo7MFNFg',
                'duration': '3:26:43'
            },
            {
                'title': 'React JS Full Course for Beginners',
                'description': 'Learn modern React.js from scratch',
                'youtube_id': 'bMknfKXIFA8',
                'duration': '11:55:27'
            }
        ]
    },
    'mobile': {
        'welcome_message': "Welcome to Mobile Development! I'm your AI tutor. I can help with iOS, Android, React Native, and more. What would you like to build today?",
        'videos': [
            {
                'title': 'iOS Development Course - Build a Twitter Clone',
                'description': 'Learn iOS development by building a real app',
                'youtube_id': 'FkP6wFeHRNk',
                'duration': '10:22:43'
            },
            {
                'title': 'Android Development for Beginners - Full Course',
                'description': 'Complete Android Studio tutorial',
                'youtube_id': 'fis26HvvDII',
                'duration': '11:36:22'
            },
            {
                'title': 'React Native Tutorial for Beginners',
                'description': 'Build cross-platform mobile apps',
                'youtube_id': '0-S5a0eXPoc',
                'duration': '2:21:37'
            }
        ]
    },
    'ai': {
        'welcome_message': "Welcome to Artificial Intelligence! I'm your AI tutor. I can help with machine learning, neural networks, deep learning, and more. What would you like to explore today?",
        'videos': [
            {
                'title': 'Machine Learning Course for Beginners',
                'description': 'Complete machine learning tutorial',
                'youtube_id': '7eh4d6sabA0',
                'duration': '7:19:11'
            },
            {
                'title': 'Deep Learning with TensorFlow',
                'description': 'Neural networks and deep learning fundamentals',
                'youtube_id': 'tPYj3fFJGjk',
                'duration': '6:55:17'
            },
            {
                'title': 'PyTorch for Deep Learning',
                'description': 'Complete PyTorch tutorial',
                'youtube_id': 'V_xro1bcAuA',
                'duration': '16:30:27'
            }
        ]
    },
    'cloud': {
        'welcome_message': "Welcome to Cloud Computing! I'm your AI tutor. I can help with AWS, Azure, cloud architecture, and more. What would you like to learn today?",
        'videos': [
            {
                'title': 'AWS Certified Cloud Practitioner Course',
                'description': 'Complete AWS certification preparation',
                'youtube_id': 'SOTamWNgDKc',
                'duration': '13:35:48'
            },
            {
                'title': 'Microsoft Azure Fundamentals',
                'description': 'Azure certification course',
                'youtube_id': 'NKEFWyqJ5XA',
                'duration': '3:23:40'
            },
            {
                'title': 'Docker and Kubernetes Tutorial',
                'description': 'Learn container orchestration',
                'youtube_id': 'bhBSlnQcq2k',
                'duration': '7:06:38'
            }
        ]
    },
    'cybersecurity': {
        'welcome_message': "Welcome to Cybersecurity! I'm your AI tutor. I can help with network security, ethical hacking, security analysis, and more. What would you like to learn today?",
        'videos': [
            {
                'title': 'Complete Ethical Hacking Course',
                'description': 'Learn ethical hacking from scratch',
                'youtube_id': 'fNzpcB7ODxQ',
                'duration': '12:22:52'
            },
            {
                'title': 'Network Security Course',
                'description': 'Complete network security tutorial',
                'youtube_id': '3Kq1MIfTWCE',
                'duration': '4:45:57'
            },
            {
                'title': 'Web Security & Bug Bounty Course',
                'description': 'Learn web application security',
                'youtube_id': 'X4eRbHgRawI',
                'duration': '5:28:43'
            }
        ]
    },
    'data': {
        'welcome_message': "Welcome to Data Science! I'm your AI tutor. I can help with data analysis, visualization, big data, and more. What would you like to explore today?",
        'videos': [
            {
                'title': 'Data Science Full Course',
                'description': 'Complete data science tutorial',
                'youtube_id': 'ua-CiDNNj30',
                'duration': '11:55:11'
            },
            {
                'title': 'Python for Data Analysis Tutorial',
                'description': 'Learn pandas and numpy',
                'youtube_id': 'vmEHCJofslg',
                'duration': '4:31:27'
            },
            {
                'title': 'Power BI Tutorial for Beginners',
                'description': 'Learn data visualization with Power BI',
                'youtube_id': 'H84UbKjxBbY',
                'duration': '3:45:43'
            }
        ]
    },
    'blockchain': {
        'welcome_message': "Welcome to Blockchain! I'm your AI tutor. I can help with blockchain basics, smart contracts, cryptocurrency, and more. What would you like to learn today?",
        'videos': [
            {
                'title': 'Blockchain Full Course',
                'description': 'Complete blockchain development tutorial',
                'youtube_id': 'gyMwXuJrbJQ',
                'duration': '32:00:45'
            },
            {
                'title': 'Solidity Tutorial - Full Course',
                'description': 'Learn smart contract development',
                'youtube_id': 'M576WGiDBdQ',
                'duration': '16:29:23'
            },
            {
                'title': 'Web3.js Tutorial',
                'description': 'Build blockchain applications with Web3',
                'youtube_id': 'xXxjRzdYIss',
                'duration': '2:16:33'
            }
        ]
    },
    'game': {
        'welcome_message': "Welcome to Game Development! I'm your AI tutor. I can help with Unity, game design, 3D modeling, and more. What would you like to create today?",
        'videos': [
            {
                'title': 'Unity Full Course for Beginners',
                'description': 'Learn Unity game development',
                'youtube_id': 'gB1F9G0JXOo',
                'duration': '17:42:55'
            },
            {
                'title': 'Unreal Engine 5 Beginner Tutorial',
                'description': 'Complete Unreal Engine course',
                'youtube_id': 'k-zMkzmduqI',
                'duration': '9:14:27'
            },
            {
                'title': 'Blender 3D Modeling Tutorial',
                'description': 'Learn 3D modeling for games',
                'youtube_id': 'nIoXOplUvAw',
                'duration': '13:51:49'
            }
        ]
    }
}

# Quiz data for each subject
quizzes = {
    'math': [
        {
            'id': 'math_quiz1',
            'title': 'Algebra Basics Quiz',
            'description': 'Test your knowledge of basic algebraic concepts',
            'questions': [
                {
                    'question': 'Solve for x: 2x + 5 = 15',
                    'options': ['x = 5', 'x = 10', 'x = 7.5', 'x = 5.5'],
                    'correct': 0,
                    'explanation': 'Subtract 5 from both sides: 2x = 10. Then divide both sides by 2: x = 5'
                },
                {
                    'question': 'Simplify the expression: 3(x + 2) - 4x',
                    'options': ['3x + 6 - 4x', '3x + 6', '-x + 6', 'None of the above'],
                    'correct': 2,
                    'explanation': '3(x + 2) - 4x = 3x + 6 - 4x = -x + 6'
                },
                {
                    'question': 'Factor the expression: x² - 9',
                    'options': ['(x + 3)(x - 3)', '(x + 9)(x - 9)', '(x + 3)²', '(x - 3)²'],
                    'correct': 0,
                    'explanation': 'x² - 9 is a difference of squares: a² - b² = (a + b)(a - b)'
                },
                {
                    'question': 'If f(x) = 2x² + 3x - 5, what is f(2)?',
                    'options': ['8', '9', '11', '13'],
                    'correct': 2,
                    'explanation': 'f(2) = 2(2)² + 3(2) - 5 = 2(4) + 6 - 5 = 8 + 6 - 5 = 9'
                },
                {
                    'question': 'Solve the inequality: 3x - 7 > 2',
                    'options': ['x > 3', 'x < 3', 'x > 3/2', 'x < 3/2'],
                    'correct': 0,
                    'explanation': '3x - 7 > 2, Add 7 to both sides: 3x > 9, Divide by 3: x > 3'
                }
            ]
        }
    ],
    'science': [
        {
            'id': 'science_quiz1',
            'title': 'Physics Fundamentals Quiz',
            'description': 'Test your knowledge of basic physics concepts',
            'questions': [
                {
                    'question': 'What is Newton\'s First Law of Motion?',
                    'options': [
                        'An object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force', 
                        'Force equals mass times acceleration', 
                        'For every action, there is an equal and opposite reaction', 
                        'Energy cannot be created or destroyed'
                    ],
                    'correct': 0,
                    'explanation': 'Newton\'s First Law of Motion is the law of inertia: objects maintain their state of motion unless acted upon by an external force.'
                },
                {
                    'question': 'What is the SI unit of force?',
                    'options': ['Joule', 'Newton', 'Watt', 'Pascal'],
                    'correct': 1,
                    'explanation': 'The SI unit of force is the Newton (N), which equals one kilogram meter per second squared.'
                },
                {
                    'question': 'What is the formula for kinetic energy?',
                    'options': ['E = mc²', 'KE = ½mv²', 'F = ma', 'p = mv'],
                    'correct': 1,
                    'explanation': 'Kinetic energy is calculated as KE = ½mv², where m is mass and v is velocity.'
                },
                {
                    'question': 'Which of these is NOT a state of matter?',
                    'options': ['Solid', 'Liquid', 'Gas', 'Energy'],
                    'correct': 3,
                    'explanation': 'The common states of matter are solid, liquid, gas, and plasma. Energy is a property, not a state of matter.'
                },
                {
                    'question': 'What type of wave requires a medium to travel through?',
                    'options': ['Light waves', 'Radio waves', 'Mechanical waves', 'Electromagnetic waves'],
                    'correct': 2,
                    'explanation': 'Mechanical waves, such as sound waves, require a medium to propagate. Electromagnetic waves can travel through a vacuum.'
                }
            ]
        }
    ],
    'programming': [
        {
            'id': 'programming_quiz1',
            'title': 'Python Basics Quiz',
            'description': 'Test your knowledge of Python programming fundamentals',
            'questions': [
                {
                    'question': 'What will be the output of print(type(5 / 2)) in Python 3?',
                    'options': ['<class \'int\'>', '<class \'float\'>', '<class \'number\'>', '<class \'double\'>'],
                    'correct': 1,
                    'explanation': 'In Python 3, division (/) always returns a float, so the type of 5 / 2 is float.'
                },
                {
                    'question': 'Which of the following is NOT a Python data type?',
                    'options': ['list', 'dictionary', 'tuple', 'array'],
                    'correct': 3,
                    'explanation': 'Array is not a built-in data type in Python (though you can use them from NumPy). The built-in sequence types are lists, tuples, and strings.'
                },
                {
                    'question': 'What does the following code do? [x for x in range(10) if x % 2 == 0]',
                    'options': ['Creates a list of odd numbers from 0 to 9', 'Creates a list of even numbers from 0 to 9', 'Creates a list of odd numbers from 1 to 10', 'Creates a list of even numbers from 1 to 10'],
                    'correct': 1,
                    'explanation': 'This is a list comprehension that creates a list of even numbers from 0 to 9: [0, 2, 4, 6, 8]'
                },
                {
                    'question': 'What\'s the difference between "==" and "is" in Python?',
                    'options': ['They are exactly the same', '"==" checks if two objects have the same value, "is" checks if they are the same object', '"is" checks if two objects have the same value, "==" checks if they are the same object', 'There is no "is" operator in Python'],
                    'correct': 1,
                    'explanation': '"==" checks value equality while "is" checks identity (if they are the same object in memory).'
                },
                {
                    'question': 'Which of these is a valid way to create a function in Python?',
                    'options': ['function my_func(): pass', 'def my_func(): pass', 'create my_func(): pass', 'func my_func(): pass'],
                    'correct': 1,
                    'explanation': 'In Python, functions are defined using the "def" keyword followed by the function name and parentheses.'
                }
            ]
        }
    ],
    'language': [
        {
            'id': 'language_quiz1',
            'title': 'Grammar and Writing Quiz',
            'description': 'Test your knowledge of grammar and writing principles',
            'questions': [
                {
                    'question': 'Which of the following is a complete sentence?',
                    'options': ['Because it was raining.', 'The dog and the cat.', 'Sarah walked to the store.', 'Running through the park.'],
                    'correct': 2,
                    'explanation': 'A complete sentence must have a subject and a verb. "Sarah walked to the store" has both.'
                },
                {
                    'question': 'Which sentence uses the correct form of the pronoun?',
                    'options': ['Give the book to John and I.', 'Give the book to John and me.', 'Give the book to me and John.', 'Give the book to myself and John.'],
                    'correct': 1,
                    'explanation': 'When a pronoun is used as an object, use the objective form (me, not I).'
                },
                {
                    'question': 'Which of the following is an example of a passive voice construction?',
                    'options': ['John wrote the letter.', 'The letter was written by John.', 'Writing is John\'s favorite hobby.', 'John writes letters every day.'],
                    'correct': 1,
                    'explanation': 'In passive voice, the subject receives the action. "The letter was written by John" is passive.'
                },
                {
                    'question': 'Which of the following is NOT one of the four main sentence types?',
                    'options': ['Declarative', 'Interrogative', 'Exclamatory', 'Subjunctive'],
                    'correct': 3,
                    'explanation': 'The four main sentence types are declarative (statements), interrogative (questions), imperative (commands), and exclamatory (exclamations). Subjunctive is a mood, not a sentence type.'
                },
                {
                    'question': 'What is the correct order of the writing process?',
                    'options': ['Drafting, Revising, Editing, Planning', 'Planning, Drafting, Editing, Revising', 'Planning, Drafting, Revising, Editing', 'Editing, Drafting, Planning, Revising'],
                    'correct': 2,
                    'explanation': 'The writing process typically follows: Planning (prewriting), Drafting, Revising, and then Editing.'
                }
            ]
        }
    ],
    'web': [
        {
            'id': 'web_quiz1',
            'title': 'Web Development Basics Quiz',
            'description': 'Test your knowledge of HTML, CSS, and JavaScript',
            'questions': [
                {
                    'question': 'What does HTML stand for?',
                    'options': ['Hyper Text Markup Language', 'High Tech Modern Language', 'Hyper Transfer Markup Language', 'Home Tool Markup Language'],
                    'correct': 0,
                    'explanation': 'HTML stands for Hyper Text Markup Language, which is the standard markup language for creating web pages.'
                },
                {
                    'question': 'Which CSS property is used to change the text color?',
                    'options': ['text-color', 'color', 'font-color', 'text-style'],
                    'correct': 1,
                    'explanation': 'The color property is used to set the color of text in CSS.'
                },
                {
                    'question': 'What is the correct way to declare a JavaScript variable?',
                    'options': ['variable name;', 'v name;', 'let name;', 'var = name;'],
                    'correct': 2,
                    'explanation': 'In modern JavaScript, we use let or const to declare variables. let name; is the correct syntax.'
                }
            ]
        }
    ],
    'mobile': [
        {
            'id': 'mobile_quiz1',
            'title': 'Mobile Development Fundamentals',
            'description': 'Test your knowledge of mobile app development',
            'questions': [
                {
                    'question': 'Which programming language is primarily used for iOS development?',
                    'options': ['Java', 'Swift', 'Kotlin', 'Python'],
                    'correct': 1,
                    'explanation': 'Swift is Apple\'s primary programming language for iOS development.'
                },
                {
                    'question': 'What is React Native?',
                    'options': ['A mobile browser', 'A cross-platform framework', 'An Android-only framework', 'An iOS-only framework'],
                    'correct': 1,
                    'explanation': 'React Native is a popular framework for building cross-platform mobile applications.'
                },
                {
                    'question': 'What is the Android equivalent of iOS\'s UIKit?',
                    'options': ['AndroidUI', 'Material Design', 'Android Layout', 'Android View'],
                    'correct': 3,
                    'explanation': 'Android View is the fundamental building block for user interface components in Android.'
                }
            ]
        }
    ],
    'ai': [
        {
            'id': 'ai_quiz1',
            'title': 'AI and Machine Learning Basics',
            'description': 'Test your knowledge of artificial intelligence concepts',
            'questions': [
                {
                    'question': 'What is machine learning?',
                    'options': ['A type of computer hardware', 'A programming language', 'A subset of artificial intelligence', 'A database system'],
                    'correct': 2,
                    'explanation': 'Machine learning is a subset of AI that enables systems to learn and improve from experience.'
                },
                {
                    'question': 'What is a neural network?',
                    'options': ['A computer network', 'A biological network', 'A mathematical model inspired by biological neural networks', 'A social network'],
                    'correct': 2,
                    'explanation': 'Neural networks are mathematical models inspired by the structure and function of biological neural networks.'
                },
                {
                    'question': 'What is supervised learning?',
                    'options': ['Learning with a teacher present', 'Learning from labeled data', 'Learning without data', 'Learning from unlabeled data'],
                    'correct': 1,
                    'explanation': 'Supervised learning is a type of machine learning where the model learns from labeled training data.'
                }
            ]
        }
    ],
    'cloud': [
        {
            'id': 'cloud_quiz1',
            'title': 'Cloud Computing Fundamentals',
            'description': 'Test your knowledge of cloud computing concepts',
            'questions': [
                {
                    'question': 'What is cloud computing?',
                    'options': ['Weather forecasting', 'Internet-based computing services', 'A type of computer', 'A programming language'],
                    'correct': 1,
                    'explanation': 'Cloud computing refers to the delivery of computing services over the internet.'
                },
                {
                    'question': 'What is IaaS?',
                    'options': ['Internet as a Service', 'Infrastructure as a Service', 'Integration as a Service', 'Intelligence as a Service'],
                    'correct': 1,
                    'explanation': 'IaaS (Infrastructure as a Service) provides virtualized computing resources over the internet.'
                },
                {
                    'question': 'Which is NOT a major cloud provider?',
                    'options': ['AWS', 'Azure', 'Google Cloud', 'Oracle Net'],
                    'correct': 3,
                    'explanation': 'AWS, Azure, and Google Cloud are major cloud providers. Oracle Net is not a cloud provider (Oracle Cloud is).'
                }
            ]
        }
    ],
    'cybersecurity': [
        {
            'id': 'security_quiz1',
            'title': 'Cybersecurity Basics',
            'description': 'Test your knowledge of cybersecurity concepts',
            'questions': [
                {
                    'question': 'What is a firewall?',
                    'options': ['A physical wall', 'A network security device', 'A type of virus', 'A backup system'],
                    'correct': 1,
                    'explanation': 'A firewall is a network security device that monitors and filters incoming and outgoing network traffic.'
                },
                {
                    'question': 'What is encryption?',
                    'options': ['Data compression', 'Data deletion', 'Converting data into a secret code', 'Data backup'],
                    'correct': 2,
                    'explanation': 'Encryption is the process of converting data into a secret code to prevent unauthorized access.'
                },
                {
                    'question': 'What is phishing?',
                    'options': ['A fishing technique', 'A type of encryption', 'A social engineering attack', 'A network protocol'],
                    'correct': 2,
                    'explanation': 'Phishing is a type of social engineering attack often used to steal user data.'
                }
            ]
        }
    ],
    'data': [
        {
            'id': 'data_quiz1',
            'title': 'Data Science Fundamentals',
            'description': 'Test your knowledge of data science concepts',
            'questions': [
                {
                    'question': 'What is data visualization?',
                    'options': ['Writing data', 'Creating visual representations of data', 'Deleting data', 'Encrypting data'],
                    'correct': 1,
                    'explanation': 'Data visualization is the graphical representation of information and data.'
                },
                {
                    'question': 'What is a dataset?',
                    'options': ['A type of database', 'A collection of related data', 'A programming language', 'A visualization tool'],
                    'correct': 1,
                    'explanation': 'A dataset is a collection of related data points or observations.'
                },
                {
                    'question': 'What is statistical analysis?',
                    'options': ['Data collection', 'Data visualization', 'Mathematical interpretation of data', 'Data storage'],
                    'correct': 2,
                    'explanation': 'Statistical analysis involves using mathematical methods to interpret and analyze data.'
                }
            ]
        }
    ],
    'blockchain': [
        {
            'id': 'blockchain_quiz1',
            'title': 'Blockchain Fundamentals',
            'description': 'Test your knowledge of blockchain technology',
            'questions': [
                {
                    'question': 'What is a blockchain?',
                    'options': ['A type of cryptocurrency', 'A distributed ledger', 'A programming language', 'A database system'],
                    'correct': 1,
                    'explanation': 'A blockchain is a distributed ledger that records transactions across a network of computers.'
                },
                {
                    'question': 'What is a smart contract?',
                    'options': ['A legal document', 'A self-executing contract with code', 'A type of cryptocurrency', 'A blockchain platform'],
                    'correct': 1,
                    'explanation': 'A smart contract is a self-executing contract with the terms directly written into code.'
                },
                {
                    'question': 'What is mining in blockchain?',
                    'options': ['Extracting minerals', 'Creating new blocks', 'Writing smart contracts', 'Sending transactions'],
                    'correct': 1,
                    'explanation': 'Mining is the process of creating new blocks in a blockchain through solving complex mathematical problems.'
                }
            ]
        }
    ],
    'game': [
        {
            'id': 'game_quiz1',
            'title': 'Game Development Basics',
            'description': 'Test your knowledge of game development concepts',
            'questions': [
                {
                    'question': 'What is a game engine?',
                    'options': ['A car engine', 'A software framework for game development', 'A type of game', 'A gaming console'],
                    'correct': 1,
                    'explanation': 'A game engine is a software framework designed to create and develop video games.'
                },
                {
                    'question': 'What is Unity?',
                    'options': ['A programming language', 'A game engine', 'A 3D modeling tool', 'A gaming console'],
                    'correct': 1,
                    'explanation': 'Unity is a popular cross-platform game engine used to create both 2D and 3D games.'
                },
                {
                    'question': 'What is a sprite in game development?',
                    'options': ['A soft drink', 'A 2D image or animation', 'A 3D model', 'A sound effect'],
                    'correct': 1,
                    'explanation': 'A sprite is a 2D image or animation that is integrated into a larger scene in game development.'
                }
            ]
        }
    ]
}

# Sample quiz results for users
quiz_results = {
    'student1': {
        'math_quiz1': {'score': 4, 'total': 5, 'completed': '2023-06-08', 'answers': [0, 2, 0, 2, 0]},
        'science_quiz1': {'score': 3, 'total': 5, 'completed': '2023-06-12', 'answers': [0, 1, 1, 2, 2]}
    },
    'student2': {
        'programming_quiz1': {'score': 5, 'total': 5, 'completed': '2023-06-10', 'answers': [1, 3, 1, 1, 1]}
    }
}

# Sample progress data
progress_data = {
    'student1': {
        'math': {'completed': 15, 'total': 25, 'score': 85, 'last_activity': '2023-06-10'},
        'science': {'completed': 20, 'total': 30, 'score': 92, 'last_activity': '2023-06-15'},
        'programming': {'completed': 8, 'total': 20, 'score': 78, 'last_activity': '2023-06-05'},
        'language': {'completed': 12, 'total': 22, 'score': 88, 'last_activity': '2023-06-12'}
    },
    'student2': {
        'math': {'completed': 10, 'total': 25, 'score': 75, 'last_activity': '2023-06-08'},
        'science': {'completed': 15, 'total': 30, 'score': 82, 'last_activity': '2023-06-14'},
        'programming': {'completed': 12, 'total': 20, 'score': 90, 'last_activity': '2023-06-10'},
        'language': {'completed': 8, 'total': 22, 'score': 79, 'last_activity': '2023-06-07'}
    }
}

# Sample user notes
user_notes = {
    'student1': {
        'math': [
            {'title': 'Algebra Formulas', 'content': 'Quadratic formula: x = (-b ± √(b² - 4ac)) / 2a', 'date': '2023-06-05'},
            {'title': 'Calculus Basics', 'content': 'Derivative of x^n is n*x^(n-1)', 'date': '2023-06-10'}
        ],
        'science': [
            {'title': 'Newton\'s Laws', 'content': '1. An object at rest stays at rest\n2. F=ma\n3. Every action has an equal and opposite reaction', 'date': '2023-06-12'}
        ]
    }
}

# Enhanced video content with proper YouTube IDs
video_content = {
    'math': [
        {'title': 'Introduction to Algebra', 'duration': '15:24', 'youtube_id': 'NybHckSEQBI', 'description': 'Learn the basics of algebra including variables, expressions, and equations.'},
        {'title': 'Calculus Fundamentals', 'duration': '22:18', 'youtube_id': 'WUvTyaaNkzM', 'description': 'Introduction to limits, derivatives, and integrals in calculus.'},
        {'title': 'Statistics for Beginners', 'duration': '18:45', 'youtube_id': 'xxpc-HPKN28', 'description': 'Learn about mean, median, mode, and basic statistical concepts.'},
        {'title': 'Geometry Concepts', 'duration': '20:12', 'youtube_id': 'bk8CVC3tQkE', 'description': 'Explore angles, shapes, and geometric principles.'}
    ],
    'science': [
        {'title': 'Introduction to Physics', 'duration': '19:32', 'youtube_id': '6wb29I_79K0', 'description': 'Overview of fundamental physics concepts and principles.'},
        {'title': 'Chemistry Basics', 'duration': '21:45', 'youtube_id': 'FSyAehMdpyI', 'description': 'Learn about atoms, elements, and the periodic table.'},
        {'title': 'Biology 101', 'duration': '24:10', 'youtube_id': 'QnQe0xW_JY4', 'description': 'Introduction to cells, genetics, and biological systems.'},
        {'title': 'Earth Science Overview', 'duration': '17:28', 'youtube_id': 'JGXi_9A__Vc', 'description': 'Explore geology, meteorology, and earth processes.'}
    ],
    'programming': [
        {'title': 'Python for Beginners', 'duration': '26:14', 'youtube_id': '_uQrJ0TkZlc', 'description': 'Learn Python programming from scratch with hands-on examples.'},
        {'title': 'JavaScript Fundamentals', 'duration': '23:50', 'youtube_id': 'W6NZfCO5SIk', 'description': 'Master the basics of JavaScript for web development.'},
        {'title': 'Data Structures Explained', 'duration': '28:35', 'youtube_id': 'zg9ih6SVACc', 'description': 'Understanding arrays, linked lists, stacks, and queues.'},
        {'title': 'Web Development Basics', 'duration': '31:22', 'youtube_id': 'PkZNo7MFNFg', 'description': 'Learn HTML, CSS, and JavaScript for building websites.'}
    ],
    'language': [
        {'title': 'Essay Writing Techniques', 'duration': '22:18', 'youtube_id': 'IN6IOxKLPP4', 'description': 'Improve your essay writing with structure and style tips.'},
        {'title': 'Grammar Essentials', 'duration': '18:45', 'youtube_id': 'xphVJNXzOX0', 'description': 'Master the rules of grammar for better writing.'},
        {'title': 'Literature Analysis', 'duration': '24:33', 'youtube_id': 'QdE5T9ggKLQ', 'description': 'Learn how to analyze and interpret literary works.'},
        {'title': 'Creative Writing Workshop', 'duration': '27:15', 'youtube_id': 'R4jt2_bsGUc', 'description': 'Develop your creative writing skills with practical exercises.'}
    ]
}

# Functions to be added to your Flask app
def setup_dashboard_routes(app):
    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('home'))
        
        current_date = datetime.now().strftime('%B %d, %Y')
        return render_template_string(
            dashboard_template,
            current_date=current_date,
            username=session['username']
        )
        
    @app.route('/add-technology')
    def add_technology():
        if 'username' not in session:
            return redirect(url_for('home'))
        
        # List of available technologies to add
        technologies = [
            {
                'id': 'web',
                'title': 'Web Development',
                'icon': 'fa-globe',
                'description': 'Learn HTML, CSS, JavaScript and modern web frameworks',
                'color': '#4CAF50'
            },
            {
                'id': 'mobile',
                'title': 'Mobile Development',
                'icon': 'fa-mobile-alt',
                'description': 'Build iOS and Android applications',
                'color': '#2196F3'
            },
            {
                'id': 'ai',
                'title': 'Artificial Intelligence',
                'icon': 'fa-brain',
                'description': 'Explore machine learning and AI concepts',
                'color': '#9C27B0'
            },
            {
                'id': 'cloud',
                'title': 'Cloud Computing',
                'icon': 'fa-cloud',
                'description': 'Master AWS, Azure, and cloud technologies',
                'color': '#03A9F4'
            },
            {
                'id': 'cybersecurity',
                'title': 'Cybersecurity',
                'icon': 'fa-shield-alt',
                'description': 'Learn network security and ethical hacking',
                'color': '#F44336'
            },
            {
                'id': 'data',
                'title': 'Data Science',
                'icon': 'fa-chart-bar',
                'description': 'Master data analysis and visualization',
                'color': '#FF9800'
            },
            {
                'id': 'blockchain',
                'title': 'Blockchain',
                'icon': 'fa-link',
                'description': 'Explore cryptocurrency and blockchain technology',
                'color': '#607D8B'
            },
            {
                'id': 'game',
                'title': 'Game Development',
                'icon': 'fa-gamepad',
                'description': 'Create games using popular engines',
                'color': '#E91E63'
            }
        ]
        
        return render_template_string(
            add_technology_template,
            technologies=technologies
        )
    
    @app.route('/profile')
    def profile():
        if 'username' not in session:
            return redirect(url_for('home'))
        return render_template_string(
            profile_template,
            username=session['username']
        )
    
    @app.route('/session/<subject>')
    def learning_session(subject):
        if 'username' not in session:
            return redirect(url_for('home'))
            
        # Define all available subjects and their content
        all_subjects = {
            'math': {
                'title': 'Mathematics',
                'welcome_message': 'Welcome to Mathematics Learning!',
                'videos': ['algebra', 'calculus', 'statistics'],
                'teacher': {'name': 'Dr. Sarah Johnson', 'title': 'Mathematics Expert'}
            },
            'science': {
                'title': 'Science',
                'welcome_message': 'Welcome to Science Learning!',
                'videos': ['physics', 'chemistry', 'biology'],
                'teacher': {'name': 'Dr. Michael Chen', 'title': 'Science Expert'}
            },
            'programming': {
                'title': 'Programming',
                'welcome_message': 'Welcome to Programming Learning!',
                'videos': ['python', 'javascript', 'java'],
                'teacher': {'name': 'Prof. Alex Turner', 'title': 'Programming Expert'}
            },
            'language': {
                'title': 'Language Arts',
                'welcome_message': 'Welcome to Language Learning!',
                'videos': ['grammar', 'writing', 'literature'],
                'teacher': {'name': 'Dr. Emily Brown', 'title': 'Language Expert'}
            },
            'web': {
                'title': 'Web Development',
                'welcome_message': 'Welcome to Web Development Learning!',
                'videos': ['html-css', 'javascript-basics', 'responsive-design'],
                'teacher': {'name': 'Prof. David Wilson', 'title': 'Web Development Expert'}
            },
            'mobile': {
                'title': 'Mobile Development',
                'welcome_message': 'Welcome to Mobile Development Learning!',
                'videos': ['ios-development', 'android-basics', 'cross-platform'],
                'teacher': {'name': 'Dr. Lisa Zhang', 'title': 'Mobile Development Expert'}
            },
            'ai': {
                'title': 'Artificial Intelligence',
                'welcome_message': 'Welcome to AI Learning!',
                'videos': ['machine-learning', 'neural-networks', 'deep-learning'],
                'teacher': {'name': 'Dr. James Foster', 'title': 'AI Expert'}
            },
            'cloud': {
                'title': 'Cloud Computing',
                'welcome_message': 'Welcome to Cloud Computing Learning!',
                'videos': ['aws-basics', 'azure-fundamentals', 'cloud-architecture'],
                'teacher': {'name': 'Prof. Maria Garcia', 'title': 'Cloud Computing Expert'}
            },
            'cybersecurity': {
                'title': 'Cybersecurity',
                'welcome_message': 'Welcome to Cybersecurity Learning!',
                'videos': ['network-security', 'ethical-hacking', 'security-analysis'],
                'teacher': {'name': 'Dr. Robert Chen', 'title': 'Cybersecurity Expert'}
            },
            'data': {
                'title': 'Data Science',
                'welcome_message': 'Welcome to Data Science Learning!',
                'videos': ['data-analysis', 'visualization', 'big-data'],
                'teacher': {'name': 'Dr. Anna Smith', 'title': 'Data Science Expert'}
            },
            'blockchain': {
                'title': 'Blockchain',
                'welcome_message': 'Welcome to Blockchain Learning!',
                'videos': ['blockchain-basics', 'smart-contracts', 'cryptocurrency'],
                'teacher': {'name': 'Prof. Michael Lee', 'title': 'Blockchain Expert'}
            },
            'game': {
                'title': 'Game Development',
                'welcome_message': 'Welcome to Game Development Learning!',
                'videos': ['unity-basics', 'game-design', '3d-modeling'],
                'teacher': {'name': 'Prof. Sarah Anderson', 'title': 'Game Development Expert'}
            }
        }
        
        # Check if subject exists
        if subject not in all_subjects:
            return redirect(url_for('dashboard'))
        
        # Get subject content
        subject_data = all_subjects[subject]
        subject_title = subject_data['title']
        welcome_message = subject_data['welcome_message']
        videos = subject_data['videos']
        teacher = subject_data['teacher']
        
        # Initialize progress data if not exists
        username = session['username']
        progress = {
            'completed': 0,
            'total': len(videos),
            'score': 0,
            'last_activity': datetime.now().strftime('%Y-%m-%d')
        }
        
        return render_template_string(
            session_template,
            subject=subject,
            subject_title=subject_title,
            welcome_message=welcome_message,
            videos=videos,
            teacher=teacher,
            progress=progress
        )
    
    @app.route('/session/<subject>/teacher', methods=['GET'])
    def get_teacher(subject):
        if subject not in teachers:
            return jsonify({'error': 'Subject not found'}), 404
        return jsonify(teachers[subject])
    
    @app.route('/api/chat/real', methods=['POST'])
    def real_chat():
        if 'username' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        data = request.json
        subject = data.get('subject')
        message = data.get('message')
        
        if not subject or not message:
            return jsonify({'error': 'Missing subject or message'}), 400
            
        response = get_ai_response(subject, message)
        return jsonify({'response': response})
    
    @app.route('/quizzes/<subject>')
    def subject_quizzes(subject):
        if 'username' not in session:
            return redirect(url_for('home'))
        if subject not in quizzes:
            return redirect(url_for('dashboard'))
            
        return render_template_string(
            quiz_list_template,
            subject=subject,
            quizzes=quizzes[subject]
        )
    
    @app.route('/quiz/<quiz_id>')
    def take_quiz(quiz_id):
        if 'username' not in session:
            return redirect(url_for('home'))
            
        # Find the quiz
        quiz = None
        for subject_quizzes in quizzes.values():
            for q in subject_quizzes:
                if q['id'] == quiz_id:
                    quiz = q
                    break
            if quiz:
                break
                
        if not quiz:
            return redirect(url_for('dashboard'))
            
        return render_template_string(
            quiz_template,
            quiz=quiz
        )
    
    @app.route('/api/submit-quiz/<quiz_id>', methods=['POST'])
    def submit_quiz(quiz_id):
        if 'username' not in session:
            return jsonify({'error': 'Not logged in'}), 401
            
        data = request.json
        answers = data.get('answers')
        
        if not answers:
            return jsonify({'error': 'No answers provided'}), 400
            
        # Find the quiz
        quiz = None
        for subject_quizzes in quizzes.values():
            for q in subject_quizzes:
                if q['id'] == quiz_id:
                    quiz = q
                    break
            if quiz:
                break
                
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
            
        # Calculate score
        score = 0
        total = len(quiz['questions'])
        for i, answer in enumerate(answers):
            if i < total and answer == quiz['questions'][i]['correct']:
                score += 1
                
        # Save result
        username = session['username']
        if username not in quiz_results:
            quiz_results[username] = {}
        quiz_results[username][quiz_id] = {
            'score': score,
            'total': total,
            'completed': datetime.now().strftime('%Y-%m-%d'),
            'answers': answers
        }
        
        return jsonify({
            'score': score,
            'total': total,
            'percentage': (score / total) * 100
        })

def get_ai_response(subject, message):
    # This is a simplified version of the function from the original app
    # In a real implementation, you would call an AI API here
    responses = {
        'math': [
            "Let's solve this math problem step by step.",
            "In mathematics, it's important to understand the underlying concepts.",
            "Would you like me to explain this mathematical concept in more detail?"
        ],
        'science': [
            "That's an interesting scientific question!",
            "Let's explore this scientific concept together.",
            "Science is all about observation and experimentation."
        ],
        'programming': [
            "Let me help you with that programming concept.",
            "Programming is about breaking down problems into smaller steps.",
            "Here's how we can solve this coding challenge."
        ],
        'language': [
            "Let's improve your writing skills.",
            "Grammar is an essential part of effective communication.",
            "Would you like to analyze this piece of literature together?"
        ]
    }
    return random.choice(responses.get(subject, ["I'm here to help you learn!"]))

# Template definitions will be added in subsequent edits

# Dashboard template
dashboard_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        :root {
            --primary-color: #4568dc;
            --secondary-color: #3f51b5;
            --accent-color: #FF5722;
            --text-color: #333;
            --light-bg: #f4f7fd;
            --card-bg: white;
            --shadow: 0 4px 20px rgba(0,0,0,0.08);
            --transition: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background-color: var(--light-bg);
            color: var(--text-color);
            line-height: 1.6;
        }
        
        .container { 
            display: flex;
            min-height: 100vh;
            position: relative;
        }
        
        /* Enhanced Main Content Styling */
        .main-content {
            flex: 1;
            margin-left: 280px;
            padding: 2rem;
            background: var(--light-bg);
        }
        
        .dashboard-header {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .greeting {
            font-size: 2rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        
        .date {
            color: #666;
            font-size: 1.1rem;
        }
        
        /* Enhanced Dashboard Stats/Cards Styling */
        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: var(--shadow);
            transition: var(--transition);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(69, 104, 220, 0.03));
            pointer-events: none;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }
        
        .stat-card:hover .subject-icon {
            transform: scale(1.1) rotate(5deg);
        }
        
        .add-tech-card {
            border: 2px dashed var(--primary-color);
            background: rgba(69, 104, 220, 0.03);
            transition: all 0.3s ease;
        }
        
        .add-tech-card:hover {
            background: rgba(69, 104, 220, 0.08);
            border-style: solid;
        }
        
        .add-tech-card .add-icon {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .add-tech-card:hover .add-icon i {
            transform: scale(1.1) rotate(180deg);
            transition: transform 0.5s ease;
        }
        
        .subject-icon {
            width: 100px;
            height: 100px;
            margin-bottom: 1.5rem;
            transition: var(--transition);
        }
        
        .stat-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary-color);
        }
        
        .stat-card p {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }
        
        /* Responsive Design */
        @media (max-width: 1024px) {
            .dashboard-stats {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .dashboard-stats {
                grid-template-columns: 1fr;
            }
            
            .greeting {
                font-size: 1.5rem;
            }
        }
        
        /* Animation Keyframes */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Apply animations */
        .dashboard-header {
            animation: fadeIn 0.6s ease-out;
        }
        
        .stat-card {
            animation: fadeIn 0.6s ease-out;
            animation-fill-mode: both;
        }
        
        .stat-card:nth-child(1) { animation-delay: 0.2s; }
        .stat-card:nth-child(2) { animation-delay: 0.4s; }
        .stat-card:nth-child(3) { animation-delay: 0.6s; }
        .stat-card:nth-child(4) { animation-delay: 0.8s; }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--light-bg);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-content" style="margin-left: 0;">
            <div class="dashboard-header">
                <div>
                    <h1 class="greeting">Welcome back, {{ session['name'] }}!</h1>
                    <p class="date">{{ current_date }}</p>
                </div>
                <div class="nav-links" style="display: flex; gap: 20px;">
                    <a href="/logout" style="text-decoration: none; color: var(--primary-color);">
                        <i class="fas fa-sign-out-alt"></i>
                        Logout
                    </a>
                </div>
            </div>
            
            <div class="dashboard-stats">
                {% for subject in ['math', 'science', 'programming', 'language'] %}
                <div class="stat-card" onclick="window.location.href='/session/{{ subject }}'">
                    <img src="/static/images/{{ subject }}-icon.svg" alt="{{ subject }}" class="subject-icon" style="width: 60px; height: 60px; object-fit: contain;">
                    <h3 class="stat-title">{{ subject.title() }}</h3>
                    <p>Click to start learning</p>
                </div>
                {% endfor %}
                
                <!-- Add More Technology Card -->
                <div class="stat-card add-tech-card" onclick="window.location.href='/add-technology'">
                    <div class="add-icon">
                        <i class="fas fa-plus-circle" style="font-size: 60px; color: var(--primary-color); margin-bottom: 15px;"></i>
                    </div>
                    <h3 class="stat-title">Add More Technology</h3>
                    <p>Explore and add new learning paths</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

# Profile template
profile_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>My Profile</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary-color: #4568dc;
            --secondary-color: #3f51b5;
            --accent-color: #B5A33F;
            --text-color: #333;
            --light-bg: #f4f7fd;
            --card-bg: white;
            --shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: var(--light-bg);
            color: var(--text-color);
        }
        
        .container { 
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 250px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 20px 0;
            position: fixed;
            height: 100vh;
            box-shadow: var(--shadow);
            z-index: 10;
        }
        
        .sidebar-header {
            padding: 0 20px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            text-align: center;
        }
        
        .profile-pic {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin: 0 auto 10px;
            display: block;
            object-fit: cover;
            border: 3px solid white;
        }
        
        .nav-menu {
            list-style: none;
            padding: 0;
            margin: 20px 0;
        }
        
        .nav-item {
            padding: 12px 20px;
            border-left: 3px solid transparent;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .nav-item:hover, .nav-item.active {
            background: rgba(255,255,255,0.1);
            border-left: 3px solid var(--accent-color);
        }
        
        .nav-item a {
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
        }
        
        .nav-icon {
            margin-right: 10px;
            width: 20px;
            text-align: center;
        }
        
        .main-content {
            flex: 1;
            margin-left: 250px;
            padding: 20px;
        }
        
        .profile-header {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
        }
        
        .large-profile-pic {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            margin-right: 30px;
            object-fit: cover;
            border: 5px solid var(--light-bg);
        }
        
        .profile-details {
            flex: 1;
        }
        
        .profile-name {
            font-size: 28px;
            font-weight: 600;
            margin: 0 0 10px;
        }
        
        .profile-role {
            font-size: 18px;
            color: #666;
            margin: 0 0 15px;
        }
        
        .profile-stats {
            display: flex;
            gap: 20px;
        }
        
        .stat {
            padding: 10px 20px;
            background: var(--light-bg);
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: 600;
        }
        
        .stat-label {
            font-size: 14px;
            color: #666;
        }
        
        .profile-section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }
        
        .section-title {
            font-size: 20px;
            margin: 0 0 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
            font-weight: 500;
        }
        
        .profile-info {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        
        .info-item {
            padding-bottom: 15px;
        }
        
        .info-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-weight: 500;
        }
        
        .button {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .edit-button {
            margin-left: auto;
        }
        
        .achievements {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 20px;
        }
        
        .achievement {
            background: var(--light-bg);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .achievement:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow);
        }
        
        .achievement-icon {
            font-size: 30px;
            margin-bottom: 10px;
        }
        
        .achievement-title {
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .achievement-date {
            font-size: 12px;
            color: #666;
        }
        
        .achievement.locked {
            opacity: 0.5;
        }
        
        .achievement.locked:hover {
            transform: none;
            box-shadow: none;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
            }
            
            .container {
                flex-direction: column;
            }
            
            .main-content {
                margin-left: 0;
            }
            
            .profile-header {
                flex-direction: column;
                text-align: center;
            }
            
            .large-profile-pic {
                margin-right: 0;
                margin-bottom: 20px;
            }
            
            .profile-info {
                grid-template-columns: 1fr;
            }
            
            .profile-stats {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="sidebar-header">
                <img src="https://ui-avatars.com/api/?name={{ user.name }}&background=random" alt="Profile" class="profile-pic">
                <h3>{{ user.name }}</h3>
                <p>{{ user.role|capitalize }}</p>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/dashboard">
                        <span class="nav-icon">📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item active">
                    <a href="/profile">
                        <span class="nav-icon">👤</span> My Profile
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/">
                        <span class="nav-icon">📚</span> Courses
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#">
                        <span class="nav-icon">📝</span> Assignments
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#">
                        <span class="nav-icon">📈</span> Progress
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#">
                        <span class="nav-icon">🏆</span> Achievements
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/logout">
                        <span class="nav-icon">🚪</span> Logout
                    </a>
                </li>
            </ul>
        </div>
        
        <div class="main-content">
            <div class="profile-header">
                <img src="https://ui-avatars.com/api/?name={{ user.name }}&size=150&background=random" alt="Profile" class="large-profile-pic">
                
                <div class="profile-details">
                    <h1 class="profile-name">{{ user.name }}</h1>
                    <p class="profile-role">{{ user.role|capitalize }}</p>
                    
                    <div class="profile-stats">
                        <div class="stat">
                            <div class="stat-value">4</div>
                            <div class="stat-label">Courses</div>
                        </div>
                        
                        <div class="stat">
                            <div class="stat-value">18</div>
                            <div class="stat-label">Completed Lessons</div>
                        </div>
                        
                        <div class="stat">
                            <div class="stat-value">5</div>
                            <div class="stat-label">Achievements</div>
                        </div>
                    </div>
                </div>
                
                <button class="button edit-button">
                    <span>✏️</span> Edit Profile
                </button>
            </div>
            
            <div class="profile-section">
                <h2 class="section-title">Personal Information</h2>
                
                <div class="profile-info">
                    <div class="info-item">
                        <div class="info-label">Username</div>
                        <div class="info-value">{{ user.username }}</div>
                    </div>
                    
                    <div class="info-item">
                        <div class="info-label">Full Name</div>
                        <div class="info-value">{{ user.name }}</div>
                    </div>
                    
                    <div class="info-item">
                        <div class="info-label">Email</div>
                        <div class="info-value">{{ user.email }}</div>
                    </div>
                    
                    <div class="info-item">
                        <div class="info-label">Member Since</div>
                        <div class="info-value">{{ user.joined }}</div>
                    </div>
                </div>
            </div>
            
            <div class="profile-section">
                <h2 class="section-title">Achievements</h2>
                
                <div class="achievements">
                    <div class="achievement">
                        <div class="achievement-icon">🏅</div>
                        <div class="achievement-title">Fast Learner</div>
                        <div class="achievement-date">Earned on May 15, 2023</div>
                    </div>
                    
                    <div class="achievement">
                        <div class="achievement-icon">🌟</div>
                        <div class="achievement-title">Perfect Score</div>
                        <div class="achievement-date">Earned on June 2, 2023</div>
                    </div>
                    
                    <div class="achievement">
                        <div class="achievement-icon">🔥</div>
                        <div class="achievement-title">3-Day Streak</div>
                        <div class="achievement-date">Earned on June 10, 2023</div>
                    </div>
                    
                    <div class="achievement">
                        <div class="achievement-icon">📚</div>
                        <div class="achievement-title">Bookworm</div>
                        <div class="achievement-date">Earned on June 22, 2023</div>
                    </div>
                    
                    <div class="achievement">
                        <div class="achievement-icon">🧩</div>
                        <div class="achievement-title">Problem Solver</div>
                        <div class="achievement-date">Earned on July 5, 2023</div>
                    </div>
                    
                    <div class="achievement locked">
                        <div class="achievement-icon">🏆</div>
                        <div class="achievement-title">Course Master</div>
                        <div class="achievement-date">Locked</div>
                    </div>
                    
                    <div class="achievement locked">
                        <div class="achievement-icon">⚡</div>
                        <div class="achievement-title">Quick Thinker</div>
                        <div class="achievement-date">Locked</div>
                    </div>
                    
                    <div class="achievement locked">
                        <div class="achievement-icon">🌈</div>
                        <div class="achievement-title">All Subjects</div>
                        <div class="achievement-date">Locked</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

# Enhanced learning session template
session_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ subject_title }} Learning Session</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f7fd; }
        .container { display: flex; height: 100vh; }
        .sidebar { width: 280px; background: linear-gradient(135deg, #4568dc, #3f51b5); color: white; display: flex; flex-direction: column; }
        .main-content { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
        .header { background: white; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .tab-container { display: flex; padding: 20px; flex: 1; overflow: hidden; }
        .tabs-sidebar { width: 200px; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-right: 20px; }
        .tab-button { padding: 12px; margin-bottom: 10px; cursor: pointer; border-radius: 8px; transition: all 0.3s; }
        .tab-button:hover { background-color: #f0f3ff; }
        .tab-button.active { background: linear-gradient(135deg, #4568dc, #3f51b5); color: white; }
        .tab-content { flex: 1; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow-y: auto; }
        
        .user-info { padding: 20px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .profile-pic { width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 10px; display: block; object-fit: cover; border: 3px solid white; }
        
        .course-info { padding: 20px; margin-top: auto; }
        .teacher-card { display: flex; align-items: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; margin-top: 15px; }
        .teacher-pic { width: 50px; height: 50px; border-radius: 50%; margin-right: 15px; object-fit: cover; }
        
        .chat-container { height: 400px; overflow-y: auto; margin-bottom: 15px; padding: 15px; border: 1px solid #eee; border-radius: 8px; }
        .chat-message { padding: 12px; margin-bottom: 12px; border-radius: 8px; max-width: 85%; position: relative; }
        .ai-message { background: #e6f7ff; margin-right: auto; border-bottom-left-radius: 2px; }
        .user-message { background: #f1f1f1; margin-left: auto; border-bottom-right-radius: 2px; }
        .message-input { display: flex; }
        input[type="text"] { flex-grow: 1; padding: 12px; border: 1px solid #ddd; border-radius: 4px; margin-right: 10px; }
        
        .button { background: linear-gradient(135deg, #4568dc, #3f51b5); color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; font-weight: 500; transition: all 0.3s ease; }
        .button:hover { background: linear-gradient(135deg, #3b5bdb, #303f9f); transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        
        .video-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .video-card { background: #f9f9f9; border-radius: 12px; overflow: hidden; transition: all 0.3s ease; }
        .video-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
        .video-thumbnail { position: relative; height: 180px; overflow: hidden; }
        .video-thumbnail img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
        .video-thumbnail:hover img { transform: scale(1.05); }
        .video-duration { position: absolute; bottom: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; }
        .video-content { padding: 15px; }
        .video-title { font-weight: 500; margin-bottom: 10px; }
        
        .notes-container { display: flex; flex-direction: column; height: 100%; }
        .notes-header { display: flex; justify-content: space-between; margin-bottom: 15px; }
        .notes-list { flex: 1; overflow-y: auto; margin-bottom: 20px; }
        .note-card { background: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        .note-title { font-weight: 500; margin-bottom: 5px; }
        .note-date { font-size: 12px; color: #999; margin-bottom: 10px; }
        .note-content { white-space: pre-wrap; }
        .new-note-form { display: flex; flex-direction: column; }
        textarea { width: 100%; min-height: 150px; padding: 12px; border: 1px solid #ddd; border-radius: 4px; resize: vertical; margin-bottom: 10px; }
        
        .resource-card { background: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        
        #video-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; justify-content: center; align-items: center; }
        .video-modal-content { width: 80%; max-width: 800px; background: white; border-radius: 12px; overflow: hidden; position: relative; }
        .close-modal { position: absolute; top: 10px; right: 15px; color: white; font-size: 30px; cursor: pointer; z-index: 1100; }
        .youtube-embed { width: 100%; height: 450px; border: none; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Side Bar -->
        <div class="sidebar">
            <!-- User Info -->
            <div class="user-info">
                <img src="https://ui-avatars.com/api/?name={{ session.get('name', 'User') }}&background=random" alt="Profile" class="profile-pic">
                <h3>{{ session.get('name', 'User') }}</h3>
                <p>{{ subject_title }} Student</p>
            </div>
            
            
            <!-- Teacher Info -->
            <div class="course-info">
                <h4>Course Information</h4>
                <p>Instructor: {{ teacher.name }}</p>
                
                <div class="teacher-card">
                    <img src="https://ui-avatars.com/api/?name={{ teacher.name }}&background=random" alt="{{ teacher.name }}" class="teacher-pic">
                    <div>
                        <div style="font-weight: 500;">{{ teacher.name }}</div>
                        <div style="font-size: 12px; opacity: 0.8;">{{ subject_title }} Teacher</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <!-- Header -->
            <div class="header">
                <h1>{{ subject_title }} Learning Session</h1>
                <div>
                    <a href="/dashboard" style="margin-right: 15px;">Dashboard</a>
                    <a href="/" style="margin-right: 15px;">Courses</a>
                    <a href="/logout">Logout</a>
                </div>
            </div>
            
            <!-- Tab Container -->
            <div class="tab-container">
                <!-- Tab Sidebar -->
                <div class="tabs-sidebar">
                    <div class="tab-button active" onclick="switchTab('chat-tab')">AI Tutor Chat</div>
                    <div class="tab-button" onclick="switchTab('videos-tab')">Video Lessons</div>
                    <div class="tab-button" onclick="switchTab('notes-tab')">Notes</div>
                    <div class="tab-button" onclick="switchTab('resources-tab')">Resources</div>
                </div>
                
                <!-- Tab Content -->
                <div class="tab-content">
                    <!-- Chat Tab -->
                    <div id="chat-tab" class="tab-pane active">
                        <h3>Chat with Your AI Tutor</h3>
                        <div id="chat-container" class="chat-container">
                            <div class="chat-message ai-message">
                                <strong>AI Tutor:</strong> {{ welcome_message }}
                            </div>
                        </div>
                        <div class="message-input">
                            <input type="text" id="user-input" placeholder="Ask your AI tutor...">
                            <button class="button" onclick="sendMessage()">Send</button>
                        </div>
                    </div>
                    
                    <!-- Videos Tab -->
                    <div id="videos-tab" class="tab-pane">
                        <h3>Video Lessons</h3>
                        <p>Watch these educational videos to enhance your learning:</p>
                        
                        <div class="video-grid">
                            {% for video in videos %}
                            <div class="video-card">
                                <div class="video-thumbnail" onclick="openVideoModal('{{ video.youtube_id }}', '{{ video.title }}')">
                                    <img src="https://img.youtube.com/vi/{{ video.youtube_id }}/mqdefault.jpg" alt="{{ video.title }}">
                                    <div class="video-duration">{{ video.duration }}</div>
                                </div>
                                <div class="video-content">
                                    <div class="video-title">{{ video.title }}</div>
                                    <p>{{ video.description }}</p>
                                    <button class="button" onclick="openVideoModal('{{ video.youtube_id }}', '{{ video.title }}')">Watch Now</button>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                        
                        <!-- Video Modal -->
                        <div id="video-modal">
                            <div class="close-modal" onclick="closeVideoModal()">&times;</div>
                            <div class="video-modal-content">
                                <iframe id="youtube-player" class="youtube-embed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Notes Tab -->
                    <div id="notes-tab" class="tab-pane">
                        <div class="notes-container">
                            <div class="notes-header">
                                <h3>Your Notes</h3>
                                <button class="button" onclick="toggleNewNoteForm()">New Note</button>
                            </div>
                            
                            <div id="notes-list" class="notes-list">
                                <!-- Notes will be loaded here dynamically -->
                                <div class="note-card">
                                    <div class="note-title">Loading your notes...</div>
                                    <div class="note-date"></div>
                                    <div class="note-content">Please wait while we fetch your notes...</div>
                                </div>
                            </div>
                            
                            <div id="new-note-form" class="new-note-form" style="display: none;">
                                <input type="text" id="note-title" placeholder="Note Title" style="margin-bottom: 10px;">
                                <textarea id="note-content" placeholder="Write your note here..."></textarea>
                                <button class="button" onclick="saveNote()">Save Note</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Resources Tab -->
                    <div id="resources-tab" class="tab-pane">
                        <h3>Additional Resources</h3>
                        <div class="resource-card">
                            <h4>Practice Problems</h4>
                            <p>Access a collection of practice problems to test your knowledge.</p>
                            <button class="button" onclick="window.location.href='/quizzes/{{ subject }}'">Start Practice</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Tab Switching
        function switchTab(tabId) {
            // Hide all tab panes
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.style.display = 'none';
            });
            
            // Remove active class from all tab buttons
            document.querySelectorAll('.tab-button').forEach(button => {
                button.classList.remove('active');
            });
            
            // Show selected tab and activate its button
            document.getElementById(tabId).style.display = 'block';
            document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');
        }
        
        // Initialize with chat tab active
        document.addEventListener('DOMContentLoaded', () => {
            switchTab('chat-tab');
            loadNotes();
        });
        
        // Chat Functionality
        const chatContainer = document.getElementById('chat-container');
        const userInput = document.getElementById('user-input');
        
        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            
            // Add user message to chat
            appendMessage('You', message, 'user-message');
            userInput.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        subject: '{{ subject }}'
                    })
                });
                
                const data = await response.json();
                if (data.error) {
                    appendMessage('System', 'Sorry, there was an error processing your request.', 'ai-message');
                } else {
                    appendMessage('AI Tutor', data.response, 'ai-message');
                }
            } catch (error) {
                appendMessage('System', 'Sorry, there was an error connecting to the server.', 'ai-message');
            }
        }
        
        function appendMessage(sender, text, className) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${className}`;
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Handle enter key in chat input
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Video Modal Functionality
        function openVideoModal(videoId, title) {
            const modal = document.getElementById('video-modal');
            const player = document.getElementById('youtube-player');
            player.src = `https://www.youtube.com/embed/${videoId}`;
            modal.style.display = 'flex';
        }
        
        function closeVideoModal() {
            const modal = document.getElementById('video-modal');
            const player = document.getElementById('youtube-player');
            player.src = '';
            modal.style.display = 'none';
        }
        
        // Notes Functionality
        async function loadNotes() {
            try {
                const response = await fetch(`/session/{{ subject }}/notes`);
                const notes = await response.json();
                
                const notesList = document.getElementById('notes-list');
                notesList.innerHTML = '';
                
                if (notes.length === 0) {
                    notesList.innerHTML = `
                        <div class="note-card">
                            <div class="note-title">No notes yet</div>
                            <div class="note-content">Click "New Note" to create your first note!</div>
                        </div>
                    `;
                    return;
                }
                
                notes.forEach(note => {
                    const noteCard = document.createElement('div');
                    noteCard.className = 'note-card';
                    noteCard.innerHTML = `
                        <div class="note-title">${note.title}</div>
                        <div class="note-date">${note.date}</div>
                        <div class="note-content">${note.content}</div>
                    `;
                    notesList.appendChild(noteCard);
                });
            } catch (error) {
                console.error('Error loading notes:', error);
            }
        }
        
        function toggleNewNoteForm() {
            const form = document.getElementById('new-note-form');
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        }
        
        async function saveNote() {
            const titleInput = document.getElementById('note-title');
            const contentInput = document.getElementById('note-content');
            
            const title = titleInput.value.trim();
            const content = contentInput.value.trim();
            
            if (!title || !content) {
                alert('Please fill in both title and content');
                return;
            }
            
            try {
                const response = await fetch(`/session/{{ subject }}/notes`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ title, content })
                });
                
                if (response.ok) {
                    titleInput.value = '';
                    contentInput.value = '';
                    toggleNewNoteForm();
                    loadNotes();
                } else {
                    alert('Error saving note');
                }
            } catch (error) {
                console.error('Error saving note:', error);
                alert('Error saving note');
            }
        }
    </script>
</body>
</html>
'''

# Add Technology template
add_technology_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Add Technology - AI Learning Platform</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        :root {
            --primary-color: #4568dc;
            --secondary-color: #3f51b5;
            --accent-color: #FF5722;
            --text-color: #333;
            --light-bg: #f4f7fd;
            --card-bg: white;
            --shadow: 0 4px 20px rgba(0,0,0,0.08);
            --transition: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background-color: var(--light-bg);
            color: var(--text-color);
            line-height: 1.6;
        }
        
        .container { 
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            border-radius: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow);
        }
        
        .header h1 {
            font-size: 2rem;
            font-weight: 600;
        }
        
        .back-button {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: var(--transition);
            text-decoration: none;
        }
        
        .back-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .tech-card {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: var(--shadow);
            transition: var(--transition);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        
        .tech-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(69, 104, 220, 0.03));
            pointer-events: none;
        }
        
        .tech-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }
        
        .tech-icon {
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            margin-bottom: 1.5rem;
            font-size: 2rem;
            color: white;
            transition: var(--transition);
        }
        
        .tech-card:hover .tech-icon {
            transform: scale(1.1) rotate(5deg);
        }
        
        .tech-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        .tech-description {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }
        
        .add-button {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: var(--transition);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .add-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
                padding: 1.5rem;
            }
            
            .tech-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Add New Technology</h1>
            <a href="/dashboard" class="back-button">
                <i class="fas fa-arrow-left"></i>
                Back to Dashboard
            </a>
        </div>
        
        <div class="tech-grid">
            {% for tech in technologies %}
            <div class="tech-card" onclick="window.location.href='/session/{{ tech.id }}'">
                <div class="tech-icon" style="background: {{ tech.color }}">
                    <i class="fas {{ tech.icon }}"></i>
                </div>
                <h3 class="tech-title">{{ tech.title }}</h3>
                <p class="tech-description">{{ tech.description }}</p>
                <button class="add-button">
                    <i class="fas fa-plus"></i>
                    Add to Dashboard
                </button>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
''' 