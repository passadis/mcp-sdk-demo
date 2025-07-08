# 🔧 Environment Configuration Guide

## ⚠️ **IMPORTANT: You need to configure environment variables!**

The MCP Document Exchange System requires Azure OpenAI credentials to work properly.

## 🚀 **Quick Setup (3 steps):**

### **1. Create your .env file**
Copy the example file:
```bash
cp .env.example .env
```

### **2. Get Azure OpenAI credentials**
1. Go to [Azure Portal](https://portal.azure.com)
2. Find your Azure OpenAI resource
3. Get your **API Key** and **Endpoint URL**
4. Note your **Model Deployment Name**

### **3. Edit your .env file**
Open `.env` and replace these placeholders:
```bash
AZURE_OPENAI_KEY=your-actual-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-model-deployment-name
```

## 🎯 **Then start the app:**
```bash
python app.py
```

## 📋 **Required Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_KEY` | Your Azure OpenAI API key | `abcd1234...` |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint | `https://myai.openai.azure.com/` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Your model deployment name | `gpt-35-turbo` |

## ⚙️ **Automated Setup:**
Run the setup script for guided configuration:
```bash
python setup.py
```

## 🔍 **Test Your Configuration:**
The web UI will show you if environment variables are missing:
- ✅ Green status = All configured
- ⚠️ Yellow status = Missing variables
- ❌ Red status = Service unavailable

## 🆘 **Don't have Azure OpenAI?**
You can still test the UI, but summarization won't work without proper credentials.

## 📝 **Sample .env file:**
```bash
AZURE_OPENAI_KEY=sk-abc123def456...
AZURE_OPENAI_ENDPOINT=https://mycompany-openai.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```
