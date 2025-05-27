# -*- coding: utf-8 -*-
"""
VAGAS_AUTOMATE > AUTOMAÇÃO PARA DISPARO DE VAGAS 
verifica os valores chave do currículo e se candidata nas vagas
compatíveis...

'OpenSource'
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

# --------------------------------------------------------------------------- #
# ... (outros imports permanecem os mesmos)

class JobApplicationAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.applied_jobs_file = 'vagas_aplicadas.csv'
        self.resume_path = None

# --------------------------------------------------------------------------- #
        # Configurações do usuário
        self.user_data = {
            'email': 'seu_email@exemplo.com',
            'senha': 'sua_senha',
            'nome_completo': 'Seu Nome Completo',
            'telefone': '(00) 00000-0000',
            'experiencia': ['Python', 'Automação', 'Selenium', 'Desenvolvimento', 'Web Scraping'],
            'formacao': 'Sua Formação Acadêmica',
            'resumo': 'Resumo profissional com habilidades relevantes'
        }

# --------------------------------------------------------------------------- #
        # Inicializar interface para upload do currículo
        self.init_upload_interface()

    def init_upload_interface(self):
        """Cria uma interface simples para upload do currículo"""
        self.root = tk.Tk()
        self.root.title("Configuração de Automação de Vagas")
        self.root.geometry("500x300")
        
        tk.Label(self.root, text="Automação de Candidatura a Vagas", font=('Arial', 14)).pack(pady=10)

# --------------------------------------------------------------------------- #
        # Frame para upload do currículo
        resume_frame = tk.LabelFrame(self.root, text="Currículo", padx=10, pady=10)
        resume_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Button(
            resume_frame, 
            text="Selecionar Currículo (PDF/DOCX)", 
            command=self.select_resume
        ).pack(pady=5)
        
        self.resume_label = tk.Label(resume_frame, text="Nenhum arquivo selecionado", fg="gray")
        self.resume_label.pack()
        
# --------------------------------------------------------------------------- #
        # Configurações adicionais
        settings_frame = tk.LabelFrame(self.root, text="Configurações", padx=10, pady=10)
        settings_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(settings_frame, text="Número máximo de candidaturas:").grid(row=0, column=0, sticky="w")
        self.max_apps_entry = tk.Entry(settings_frame)
        self.max_apps_entry.insert(0, "5")
        self.max_apps_entry.grid(row=0, column=1, sticky="e")
# --------------------------------------------------------------------------- #
        # Botão de iniciar
        tk.Button(
            self.root, 
            text="Iniciar Automação", 
            command=self.start_automation,
            bg="green",
            fg="white"
        ).pack(pady=20)
        
        self.root.mainloop()

    def select_resume(self):
        """Seleciona o arquivo do currículo"""
        filetypes = (
            ('PDF files', '*.pdf'),
            ('Word documents', '*.docx'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title="Selecione seu currículo",
            initialdir=os.path.expanduser('~'),
            filetypes=filetypes
        )
        
        if filename:
            self.resume_path = filename
            self.resume_label.config(text=os.path.basename(filename), fg="green")
        else:
            self.resume_label.config(text="Nenhum arquivo selecionado", fg="gray")

    def start_automation(self):
        """Inicia o processo de automação após configurar a interface"""
        try:
            max_applications = int(self.max_apps_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido para o máximo de candidaturas")
            return
            
        if not self.resume_path:
            if not messagebox.askyesno("Confirmação", "Nenhum currículo foi selecionado. Deseja continuar sem enviar currículo?"):
                return
        
        self.root.destroy()  # Fecha a interface
        self.initialize_driver()
        self.initialize_csv()
        self.run(max_applications)
        
# --------------------------------------------------------------------------- #
    # ... (os outros métodos permanecem os mesmos até apply_to_job)

    def apply_to_job(self, job_info):
        """Tenta se candidatar a uma vaga com suporte a upload de currículo"""
        try:
            self.driver.get(job_info['link'])
            time.sleep(random.uniform(3, 6))
            
            if self.check_captcha():
                return False
            
# --------------------------------------------------------------------------- #
            # Tentar encontrar botão de aplicação
            apply_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@id, 'applyButton') or contains(text(), 'Aplicar')]")))
            self.safe_click(apply_button)
            time.sleep(random.uniform(2, 4))
            
# --------------------------------------------------------------------------- #
            # Verificar tipo de formulário
            form_type = self.detect_form_type()
            
            if form_type == "indeed":
                success = self.fill_indeed_form()
            elif form_type == "external":
                success = self.fill_external_form()
            else:
                success = self.fill_generic_form()
            
            if success:
                print(f"✅ Candidatura enviada para: {job_info['titulo']} na {job_info['empresa']}")
                self.save_application(job_info, 'Aplicado')
                return True
            else:
                self.save_application(job_info, 'Falha na aplicação')
                return False
                
        except Exception as e:
            print(f"⚠️ Não foi possível aplicar para esta vaga: {str(e)}")
            self.save_application(job_info, 'Falha na aplicação')
            return False

    def detect_form_type(self):
        """Detecta o tipo de formulário de candidatura"""
        try:
            
# --------------------------------------------------------------------------- #
            # Verifica se é formulário do Indeed
            if self.driver.find_elements(By.ID, "indeed-apply-widget"):
                return "indeed"

# --------------------------------------------------------------------------- #
            # Verifica se é formulário externo (redirecionamento)
            if self.driver.find_elements(By.XPATH, "//iframe[contains(@id, 'indeed-apply')]"):
                return "external"
            
# --------------------------------------------------------------------------- #
            # Formulário genérico
            return "generic"
        except:
            return "generic"

    def fill_indeed_form(self):
        """Preenche formulário do Indeed com upload de currículo"""
        try:
            
# --------------------------------------------------------------------------- #
            # Preencher informações básicas
            self.fill_basic_info()
            
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
            # Upload do currículo se disponível
            if self.resume_path:
                try:
                    upload = self.driver.find_element(By.XPATH, "//input[@type='file']")
                    upload.send_keys(self.resume_path)
                    time.sleep(random.uniform(2, 4))
                except:
                    print("⚠️ Não foi possível fazer upload do currículo")
                    
# --------------------------------------------------------------------------- #
            # Continuar para próxima etapa
            continue_button = self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Continuar') or contains(text(), 'Next')]")
            self.safe_click(continue_button)
            time.sleep(random.uniform(2, 3))
            
# --------------------------------------------------------------------------- #
            # Preencher perguntas adicionais
            self.fill_additional_questions()
            
# --------------------------------------------------------------------------- #
            # Enviar candidatura
            submit_button = self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Enviar candidatura') or contains(text(), 'Submit application')]")
            self.safe_click(submit_button)
            time.sleep(random.uniform(3, 5))
            
            return True
        except Exception as e:
            print(f"Erro no formulário do Indeed: {str(e)}")
            return False

    def fill_external_form(self):
        """Tenta preencher formulário externo (iframe)"""
        try:
            
# --------------------------------------------------------------------------- #
            # Mudar para o iframe do formulário externo
            iframe = self.driver.find_element(By.XPATH, "//iframe[contains(@id, 'indeed-apply')]")
            self.driver.switch_to.frame(iframe)
            time.sleep(2)
            
# --------------------------------------------------------------------------- #
            # Tentar preencher informações básicas
            self.fill_basic_info()
            
# --------------------------------------------------------------------------- #
            # Tentar fazer upload do currículo
            if self.resume_path:
                try:
                    upload = self.driver.find_element(By.XPATH, "//input[@type='file']")
                    upload.send_keys(self.resume_path)
                    time.sleep(random.uniform(2, 4))
                except:
                    print("⚠️ Não foi possível fazer upload do currículo no formulário externo")
                    
# --------------------------------------------------------------------------- #
            # Tentar enviar
            try:
                submit_button = self.driver.find_element(
                    By.XPATH, "//button[contains(text(), 'Submit') or contains(@type, 'submit')]")
                self.safe_click(submit_button)
                time.sleep(random.uniform(3, 5))
                
# --------------------------------------------------------------------------- #
                # Voltar para o contexto principal
                self.driver.switch_to.default_content()
                return True
            except:
                self.driver.switch_to.default_content()
                return False
                
        except Exception as e:
            print(f"Erro no formulário externo: {str(e)}")
            self.driver.switch_to.default_content()
            return False

    def fill_generic_form(self):
        """Preenche formulário genérico"""
        try:
            self.fill_basic_info()
            
# --------------------------------------------------------------------------- #
            # Tentar upload em formulário genérico
            if self.resume_path:
                try:
                    upload = self.driver.find_element(By.XPATH, "//input[@type='file']")
                    upload.send_keys(self.resume_path)
                    time.sleep(random.uniform(2, 4))
                except:
                    print("⚠️ Não foi possível fazer upload do currículo no formulário genérico")
                    
# --------------------------------------------------------------------------- #
            # Tentar enviar
            submit_button = self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Submit') or contains(@type, 'submit')]")
            self.safe_click(submit_button)
            time.sleep(random.uniform(3, 5))
            
            return True
        except Exception as e:
            print(f"Erro no formulário genérico: {str(e)}")
            return False

    def fill_basic_info(self):
        """Preenche informações básicas em qualquer formulário"""
        try:
            
# --------------------------------------------------------------------------- #
            # Nome
            name_field = self.wait.until(EC.presence_of_element_located(
                (By.NAME, "applicant.name")))
            self.human_type(name_field, self.user_data['nome_completo'])
            
            # Email
            email_field = self.driver.find_element(By.NAME, "applicant.email")
            self.human_type(email_field, self.user_data['email'])
            
            # Telefone
            phone_field = self.driver.find_element(By.NAME, "applicant.phoneNumber")
            self.human_type(phone_field, self.user_data['telefone'])
            
            time.sleep(random.uniform(1, 2))
        except:
            pass

    def fill_additional_questions(self):
        """Preenche perguntas adicionais no formulário"""
        try:
            # Experiência
            experience_field = self.driver.find_element(By.NAME, "applicant.experience")
            self.human_type(experience_field, ", ".join(self.user_data['experiencia']))
            
            # Formação
            education_field = self.driver.find_element(By.NAME, "applicant.education")
            self.human_type(education_field, self.user_data['formacao'])
            
            # Resumo
            try:
                summary_field = self.driver.find_element(By.NAME, "applicant.summary")
                self.human_type(summary_field, self.user_data['resumo'])
            except:
                pass
                
            time.sleep(random.uniform(1, 2))
        except:
            pass
        
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    automation = JobApplicationAutomation()
# --------------------------------------------------------------------------- #

