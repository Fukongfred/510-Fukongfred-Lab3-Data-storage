# Techin-510-LAB3
# ChatGPT Prompt Store

A webapp to store and quickly access your favorite ChatGPT prompts✨.

## Get started
```
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run app.py
```

## Lessons Learned
- Different types of data (structured, semi-structured, and unstructured)
- Types of storage engines (memory, file, client-server)
- How to represent data in Python using primitives and collections
- Ways to interact with database systems including SQL, ORM, database-specific drivers
- Use Pandas for database operations.

## Questions
- In the actual development of UI interfaces and interactions, is it necessary to use a platform such as streamlit? For example, if I want to design some UI components and user interactions that are not available in streamlit, how do I need to do it?

## TODO
1. CRUD prompts
    1. Create new prompts
    2. List prompts
    3. Show a single prompt
    4. Update a prompt
    5. Delete a prompt
2. Search prompts
3. Add/Remove prompts from favorite
4. Sort and filter prompts
5. Store the prompts as templates, and include some UI to render the templates into final prompt that can be copy pasted into ChatGPT