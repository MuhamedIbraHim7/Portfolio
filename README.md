# AI Engineer Portfolio

Professional portfolio website for Mohamed Ibrahim - Junior AI Engineer specializing in production-grade AI systems, RAG chatbots, and Azure Cloud deployments.

## 🌐 Live Website

**https://muhamedibrahim7.github.io/Portfolio/**

## 📋 Features

- ✨ Clean, professional design with dark/light theme
- 🎯 Detailed work experience timeline
- 🚀 Project showcase with tech stacks
- 📜 Certifications and achievements
- 📱 Fully responsive (mobile-friendly)
- 🎨 Smooth scroll animations
- 💼 Downloadable CV/Resume
- 🔗 Professional Lucide icons

## 🛠️ Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **JavaScript** - Interactive functionality
- **Lucide Icons** - Professional icon library
- **GitHub Pages** - Free hosting

## 📁 Project Structure

```
Portfolio/
├── .github/
│   └── workflows/
│       └── deploy.yml                    # GitHub Actions deployment
├── index.html                             # Main HTML structure
├── style.css                              # All styling
├── script.js                              # Interactive functionality
├── Mohamed_Ibrahim_Junior_AI_Engineer.pdf # Resume/CV
└── README.md                              # This file
```

## 🚀 Deployment

This portfolio is automatically deployed to GitHub Pages using GitHub Actions.

### Automatic Deployment

Every push to the `main` branch triggers automatic deployment:

1. **Push changes** to the `main` branch
2. GitHub Actions automatically builds and deploys
3. Changes are live at **https://muhamedibrahim7.github.io/Portfolio/** within 1-2 minutes

### Manual Deployment

You can also trigger deployment manually:

1. Go to **Actions** tab in GitHub
2. Select **Deploy to GitHub Pages** workflow
3. Click **Run workflow**

## 📝 Local Development

To run this portfolio locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MuhamedIbraHim7/Portfolio.git
   cd Portfolio
   ```

2. **Open in browser:**
   ```bash
   # On macOS
   open index.html
   
   # On Linux
   xdg-open index.html
   
   # On Windows
   start index.html
   ```

Or use a local server:
```bash
# Python 3
python -m http.server 8000

# Node.js (with http-server)
npx http-server
```

Then visit `http://localhost:8000`

## 🎨 Customization

### Update Content

1. **Edit HTML** (`index.html`) - Update text, links, and structure
2. **Edit CSS** (`style.css`) - Change colors, fonts, and layout
3. **Edit JS** (`script.js`) - Modify interactive behavior

### Change Theme Colors

Edit CSS variables in `style.css`:

```css
:root {
    --bg-primary: #0f0f0f;      /* Dark background */
    --bg-secondary: #1a1a1a;    /* Card background */
    --text-primary: #e0e0e0;    /* Main text color */
    --text-secondary: #a0a0a0;  /* Secondary text */
    --accent: #4a9eff;          /* Accent/link color */
    --border: #2a2a2a;          /* Border color */
}
```

### Add New Sections

1. Add HTML section in `index.html`
2. Add corresponding styles in `style.css`
3. Update navigation links

## 📄 License

This portfolio template is open source and free to use.

## 👤 Author

**Mohamed Ibrahim**
- Email: mohamed3ibrahim20@gmail.com
- LinkedIn: [mohamedibrahim18](https://linkedin.com/in/mohamedibrahim18)
- GitHub: [MuhamedIbraHim7](https://github.com/MuhamedIbraHim7)

## 🙏 Acknowledgments

- Icons by [Lucide](https://lucide.dev/)
- Fonts by [Google Fonts](https://fonts.google.com/)
- Hosted on [GitHub Pages](https://pages.github.com/)

---

⭐ If you like this portfolio, feel free to star the repository!
