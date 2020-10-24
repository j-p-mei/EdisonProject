curl --include --request POST \
--header "application/x-www-form-urlencoded" \
--data-binary "grant_type=client_credentials&client_id=28cde0a8-2577-4f89-a616-3fdfab78d006&client_secret=a2f65722-c646-4b22-887c-be3c19e77992" \
"https://api.tcgplayer.com/token" > reponse.txt
