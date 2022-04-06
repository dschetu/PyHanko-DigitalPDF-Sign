from dataclasses import fields
from pyhanko import stamp
from pyhanko.sign.fields import append_signature_field
from pyhanko.pdf_utils import text
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, fields

#Using a simple signer 
cms_signer = signers.SimpleSigner.load(
    key_file='selfsigned.key.pem',
    cert_file='selfsigned.cert.pem',
    key_passphrase=b'secret',
    )

#Opening a document as a binary file
with open('document.pdf', 'rb+') as doc:
    w = IncrementalPdfFileWriter(doc)
    ap= append_signature_field(w, sig_field_spec=fields.SigFieldSpec('field-name', 
    box=(72, 500, 400, 550)))
    w.write_in_place()

    #Meta data of a signature field
    meta = signers.PdfSignatureMetadata(field_name='field-name')

    #Signature field specifications
    pdf_signer = signers.PdfSigner(
        meta, signer=cms_signer,stamp_style=stamp.TextStampStyle(
        stamp_text='Signature Field!\nSigned by: %(signer)s\nTime: %(ts)s\nURL: %(url)s',
        text_box_style=text.TextBoxStyle(
        font=opentype.GlyphAccumulatorFactory('NotoSans-Regular.ttf'))))

    with open('document-signed.pdf', 'wb') as outf:
        pdf_signer.sign_pdf(w, output=outf, appearance_text_params={'url': 'https://www.yoursite.com'})

    
