# 🚀 GitHub Repository Setup for HACS

This guide will help you set up your GitHub repository to make the Bluestar AC integration available through HACS.

## 📋 Prerequisites

- **GitHub account** with a verified email
- **Git** installed on your local machine
- **Basic Git knowledge** (clone, commit, push, tags)

## 🏗️ Repository Setup

### 1. Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New repository"**
3. **Fill in the details**:
   - **Repository name**: `homeassistant-bluestar-ac`
   - **Description**: `Home Assistant integration for Bluestar Smart AC units`
   - **Visibility**: Public (required for HACS)
   - **Initialize with**: Check "Add a README file"
4. **Click "Create repository"**

### 2. Clone and Setup Local Repository

```bash
# Clone your repository
git clone https://github.com/sankarhansdah/homeassistant-bluestar-ac.git
cd homeassistant-bluestar-ac

# Copy all the integration files
cp -r custom_components/bluestar_ac ./
cp -r .github ./
cp *.md ./
cp *.json ./
cp *.yml ./
cp LICENSE ./

# Remove the original directories
rm -rf custom_components/
rm -rf bluestar_main_decompiled/
rm -rf work/
rm -rf venv/
rm -rf .venv/
rm -f *.py
rm -f *.sh
rm -f *.log
```

### 3. Update Repository URLs

Update all files to use your actual GitHub username:

```bash
# Replace 'sankarhansdah' with your actual GitHub username
find . -type f -name "*.md" -exec sed -i '' 's/sankarhansdah/YOUR_ACTUAL_USERNAME/g' {} \;
find . -type f -name "*.json" -exec sed -i '' 's/sankarhansdah/YOUR_ACTUAL_USERNAME/g' {} \;
find . -type f -name "*.yml" -exec sed -i '' 's/sankarhansdah/YOUR_ACTUAL_USERNAME/g' {} \;
```

### 4. Initial Commit and Push

```bash
# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Bluestar AC Home Assistant integration"

# Push to GitHub
git push origin main
```

## 🏷️ Create First Release

### 1. Create and Push Tag

```bash
# Create version tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial release"

# Push tag
git push origin v1.0.0
```

### 2. GitHub Actions

The repository includes GitHub Actions that will:
- **Automatically create releases** when you push tags
- **Validate HACS compatibility**
- **Upload release assets**

## 🔧 Repository Configuration

### 1. Repository Settings

1. **Go to Settings** → **General**
2. **Enable Issues** and **Wikis** if desired
3. **Set up branch protection** for main branch (optional)

### 2. GitHub Pages (Optional)

1. **Go to Settings** → **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: main, folder: / (root)
4. **Save**

## 📚 Documentation Structure

Your repository should now have this structure:

```
homeassistant-bluestar-ac/
├── bluestar_ac/                    # Integration files
│   ├── __init__.py
│   ├── const.py
│   ├── bluestar_client.py
│   ├── climate.py
│   ├── fan.py
│   ├── switch.py
│   ├── config_flow.py
│   ├── manifest.json
│   ├── README.md
│   └── translations/
│       └── en/
│           └── strings.json
├── .github/                        # GitHub Actions
│   └── workflows/
│       ├── release.yml
│       └── validate.yml
├── README.md                       # Main documentation
├── HACS_INSTALLATION.md            # Installation guide
├── CHANGELOG.md                    # Version history
├── hacs.json                       # HACS metadata
├── LICENSE                         # MIT license
└── .gitignore                     # Git ignore file
```

## 🎯 HACS Integration

### 1. Test HACS Installation

1. **In Home Assistant**, go to HACS → Integrations
2. **Add custom repository**:
   - Repository: `sankarhansdah/homeassistant-bluestar-ac`
   - Category: Integration
3. **Search for "Bluestar AC"**
4. **Install the integration**

### 2. Verify Installation

- Integration appears in HACS
- Can be installed without errors
- Configuration flow works properly
- All entities are created correctly

## 🔄 Maintenance

### 1. Updating the Integration

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main

# Create new release
git tag -a v1.1.0 -m "Release v1.1.0: New features"
git push origin v1.1.0
```

### 2. Managing Issues

- **Monitor GitHub Issues** for user problems
- **Respond promptly** to user questions
- **Update documentation** based on common issues

### 3. Community Engagement

- **Respond to discussions**
- **Help users** with installation issues
- **Share updates** in Home Assistant forums

## 📈 Growing Your Repository

### 1. Add Features

- **New AC control features**
- **Additional entity types**
- **Enhanced automation support**
- **Better error handling**

### 2. Improve Documentation

- **Add screenshots** of the integration
- **Create video tutorials**
- **Add troubleshooting guides**
- **Include automation examples**

### 3. Community Building

- **Encourage users** to star the repository
- **Ask for feedback** on new features
- **Create discussions** for feature requests
- **Share success stories**

## 🎉 Success Metrics

Your repository is successful when:

- ✅ **HACS installation** works smoothly
- ✅ **Users can configure** the integration easily
- ✅ **All features work** as expected
- ✅ **Documentation is clear** and helpful
- ✅ **Issues are resolved** promptly
- ✅ **Community is engaged** and helpful

## 🆘 Getting Help

If you need help with:

- **GitHub setup**: Check GitHub documentation
- **HACS integration**: Review HACS developer docs
- **Home Assistant**: Check HA developer documentation
- **Community support**: Ask in Home Assistant forums

---

**Your Bluestar AC integration is now ready for the world! 🌍✨**

*Make it easy for others to control their ACs from Home Assistant!* 🏠❄️
