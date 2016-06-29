# PacktpubToKindle
This python script will synchronize Packtpub's daily free-eBooks to your Kindle.

## Description
It claims the daily free eBook, then sends directly to your Kindle in mobi format.

## Supported Python Version
Tested on 2.7.x and 3.5.2

## Prerequisites
* You need to add 'kindle@packtpub.com' account to your approved personal document e-mail list in kindle settings.
* You can find the list in kindle website -> 'Manage Your Content and Devices' -> 'Settings' -> 'Personal Document Settings'
* Once you added the account, running this script will do the rest.
* Also, you need to get at least one Packtpub account. If you don't have it, create one:)

## Configurations
In config/user,
* user.email is your Packtpub's account (email).
* user.kindle is your Kindle account (Account name only e.g. user@kindle.com then use 'user').
* user.password is your Packtpub account's password.

## Notes
It is possible if the script is executed several times on the same book, Kindle will have several same documents in the library. Thus, I put a simple code to ask whether continue sending in case when the book has already been sent before. It is bad idea when someone tries to run this script automatically.