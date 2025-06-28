# Burp Setup

export https_proxy="http://localhost:8080"

curl --output burp-ca.der http://localhost:8080/cert

openssl x509 -inform der -in burp-ca.der -out burp-ca.cer


# GCloud CLI does validate no self-signed certificates and the CN/Subject match as expected
export CLOUDSDK_CORE_custom_ca_certs_file="burp-ca.cer"

# Alternative is to disable validation entirely but you do get annoying warning messages
#	gcloud config set auth/disable_ssl_validation  True

# Another gcloud alternative would be a custom profile with a gcloud config for custom_ca_certs_file
# Environment variables are handy so you can easily open a new tab with no Burp applied to test connections