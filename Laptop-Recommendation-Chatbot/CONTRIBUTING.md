# Contributing to Laptop Recommendation Chatbot

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists
- Describe the feature clearly
- Explain why it would be useful
- Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages (`git commit -m 'Add: New feature description'`)
6. Push to your fork (`git push origin feature/YourFeature`)
7. Open a Pull Request

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions small and focused

**TypeScript/React:**
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable

### Testing

Before submitting:
- Run `python test_chat_working.py` to verify backend
- Test the chat interface manually
- Check for console errors
- Verify mobile responsiveness (if frontend changes)

### Commit Message Format

```
Type: Brief description

Detailed explanation (if needed)

Examples:
- Add: New laptop comparison feature
- Fix: CORS issue with HTML interface
- Update: README with installation steps
- Refactor: Conversation manager logic
```

### Areas for Contribution

**High Priority:**
- Add more Pakistani laptops to database
- Improve recommendation algorithm
- Add Urdu language support
- Mobile app version
- Better error handling

**Medium Priority:**
- Add unit tests
- Improve UI/UX
- Add more e-commerce scrapers
- Performance optimization

**Low Priority:**
- Documentation improvements
- Code refactoring
- Additional features

## Development Setup

1. Clone your fork
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r backend/requirements.txt`
5. Run backend: `python backend/main.py`
6. Test: `python test_chat_working.py`

## Questions?

Feel free to:
- Open an issue for discussion
- Email: abbastouqeer399@gmail.com
- Comment on existing issues

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the project

Thank you for contributing! 🙏
