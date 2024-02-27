import argostranslate.package
import argostranslate.translate

class Translate:
    def __init__(self, from_code: str, to_code: str): 
        self.from_code = from_code
        self.to_code = to_code
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        # Ниже нужно исправить поля доступа к кодам языков
        package_to_install = next(
            filter(
                lambda x: x.from_code == self.from_code and x.to_code == self.to_code,  # Исправлен доступ к атрибутам
                available_packages
            ),
            None
        )
        if package_to_install:
            argostranslate.package.install_from_path(package_to_install.download())
        else:
            raise Exception("Translation package not found.")
    def translate(self, text: str):
        """
        Перевод текста.
        """
        translation_models = argostranslate.translate.get_installed_languages()
        from_model = next(filter(lambda x: x.code == self.from_code, translation_models), None)
        to_model = next(filter(lambda x: x.code == self.to_code, translation_models), None)
        
        
        if from_model and to_model:
            translation = from_model.get_translation(to_model)
            translated_text = translation.translate(text)
            return translated_text
        else:
            raise Exception("Translation models not found.")

