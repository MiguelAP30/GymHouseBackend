import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import traceback
import ssl

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")

        if not all([self.smtp_server, self.sender_email, self.sender_password]):
            print("ADVERTENCIA: Credenciales de correo electrónico no configuradas correctamente")
            return

    def send_verification_email(self, to_email: str, verification_code: str) -> bool:
        try:
            if not all([self.smtp_server, self.sender_email, self.sender_password]):
                print("Error: Credenciales de correo no configuradas")
                return False

            subject = "Verificación de cuenta - GymHouse"
            body = f"""
            <html>
              <head>
                <style>
                  body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6; 
                    color: #333; 
                    margin: 0;
                    padding: 0;
                  }}
                  .container {{ 
                    max-width: 600px; 
                    margin: 0 auto; 
                    padding: 20px; 
                    background-color: #f9f9f9;
                  }}
                  .header {{ 
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 20px; 
                    text-align: center; 
                    border-radius: 5px 5px 0 0;
                  }}
                  .content {{ 
                    padding: 20px; 
                    background-color: white;
                    border-radius: 0 0 5px 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                  }}
                  .verification-code {{ 
                    font-size: 32px; 
                    font-weight: bold; 
                    color: #4CAF50; 
                    text-align: center; 
                    padding: 20px; 
                    margin: 20px 0;
                    background-color: #f0f9f0;
                    border-radius: 5px;
                    letter-spacing: 5px;
                  }}
                  .footer {{ 
                    text-align: center; 
                    font-size: 12px; 
                    color: #777; 
                    margin-top: 20px;
                    padding: 20px;
                  }}
                  .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                  }}
                </style>
              </head>
              <body>
                <div class="container">
                  <div class="header">
                    <h1>¡Bienvenido a GymHouse!</h1>
                  </div>
                  <div class="content">
                    <h2>Verifica tu cuenta</h2>
                    <p>Gracias por registrarte en GymHouse. Para completar tu registro, por favor verifica tu cuenta usando el siguiente código:</p>
                    
                    <div class="verification-code">{verification_code}</div>
                    
                    <p>Ingresa este código en la aplicación para verificar tu cuenta.</p>
                    
                    <p>Si no solicitaste este registro, por favor ignora este correo.</p>
                  </div>
                  <div class="footer">
                    <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                    <p>© 2024 GymHouse. Todos los derechos reservados.</p>
                  </div>
                </div>
              </body>
            </html>
            """

            msg = MIMEMultipart()
            msg["From"] = f"GymHouse <{self.sender_email}>"
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            try:
                # Intentar primero con SSL (puerto 465)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, 465, context=context) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                return True
            except Exception as ssl_error:
                try:
                    # Si falla SSL, intentar con TLS (puerto 587)
                    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                        server.starttls(context=ssl.create_default_context())
                        server.login(self.sender_email, self.sender_password)
                        server.send_message(msg)
                    return True
                except Exception as tls_error:
                    print(f"Error al enviar el correo: {str(tls_error)}")
                    return False
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error al enviar el correo: {str(e)}")
            print(f"Detalles del error: {error_details}")
            return False

    def send_password_reset_code(self, to_email: str, reset_code: str) -> bool:
        try:
            if not all([self.smtp_server, self.sender_email, self.sender_password]):
                print("Error: Credenciales de correo no configuradas")
                return False

            subject = "Restablecimiento de contraseña - GymHouse"
            body = f"""
            <html>
              <head>
                <style>
                  body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6; 
                    color: #333; 
                    margin: 0;
                    padding: 0;
                  }}
                  .container {{ 
                    max-width: 600px; 
                    margin: 0 auto; 
                    padding: 20px; 
                    background-color: #f9f9f9;
                  }}
                  .header {{ 
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 20px; 
                    text-align: center; 
                    border-radius: 5px 5px 0 0;
                  }}
                  .content {{ 
                    padding: 20px; 
                    background-color: white;
                    border-radius: 0 0 5px 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                  }}
                  .reset-code {{ 
                    font-size: 32px; 
                    font-weight: bold; 
                    color: #4CAF50; 
                    text-align: center; 
                    padding: 20px; 
                    margin: 20px 0;
                    background-color: #f0f9f0;
                    border-radius: 5px;
                    letter-spacing: 5px;
                  }}
                  .footer {{ 
                    text-align: center; 
                    font-size: 12px; 
                    color: #777; 
                    margin-top: 20px;
                    padding: 20px;
                  }}
                  .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                  }}
                </style>
              </head>
              <body>
                <div class="container">
                  <div class="header">
                    <h1>Restablecimiento de contraseña</h1>
                  </div>
                  <div class="content">
                    <h2>Tu código de restablecimiento</h2>
                    <p>Has solicitado restablecer tu contraseña en GymHouse. Para continuar, utiliza el siguiente código:</p>
                    
                    <div class="reset-code">{reset_code}</div>
                    
                    <p>Ingresa este código en la aplicación para restablecer tu contraseña.</p>
                    
                    <p>Si no solicitaste este cambio, por favor ignora este correo y asegúrate de que tu cuenta esté segura.</p>
                  </div>
                  <div class="footer">
                    <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                    <p>© 2024 GymHouse. Todos los derechos reservados.</p>
                  </div>
                </div>
              </body>
            </html>
            """

            msg = MIMEMultipart()
            msg["From"] = f"GymHouse <{self.sender_email}>"
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            try:
                # Intentar primero con SSL (puerto 465)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, 465, context=context) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                return True
            except Exception as ssl_error:
                try:
                    # Si falla SSL, intentar con TLS (puerto 587)
                    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                        server.starttls(context=ssl.create_default_context())
                        server.login(self.sender_email, self.sender_password)
                        server.send_message(msg)
                    return True
                except Exception as tls_error:
                    print(f"Error al enviar el correo: {str(tls_error)}")
                    return False
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error al enviar el correo: {str(e)}")
            print(f"Detalles del error: {error_details}")
            return False 