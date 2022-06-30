# Awsume Yubikey Plugin

This is a plugin that enables you to use your Yubikey to authenticate the MFA setup on roles when assuming them.

## Installation

### Prerequisites

First you must install `swig` using your operating systems package manager:
For example, on MacOS you can use `brew`:

```
brew install swig
```

### Plugin install

```
pip install awsume-yubi-plugin
```

If you've installed awsume with `pipx`, this will install the console plugin in awsume's virtual environment:

```
pipx inject awsume awsume-yubi-plugin
```

If you've installed awsume with `brew`, you will first need to activate the `venv` that awsume is installed into:

```
source $(brew --prefix awsume)/libexec/bin/activate
pip install awsume-yubi-plugin
deactivate
```

## Usage

- First you must setup your AWS account to use a virtual MFA device that uses the Yubikey Oath service: https://aws.amazon.com/blogs/security/enhance-programmatic-access-for-iam-users-using-yubikey-for-multi-factor-authentication/

- Make sure your Yubikey is inserted before running the command.

- Use the Yubikey Oath credentials to provide an MFA token
  - `awsume <profile_name> -y` Will ask you to touch your Yubikey when authenticating the specified profile.
