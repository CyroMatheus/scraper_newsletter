from source import models
from source.logger import Log
from source.temp_page import tempPage
import inspect, asyncio, importlib, threading

async def main(model):
    nmodels = [model[0] for model in inspect.getmembers(models, inspect.isclass)]

    if model in nmodels:
        modulo = importlib.import_module('source.models')
        classModel = getattr(modulo, model)
        classModel = classModel(Log(model))
        
        temp_page = tempPage(model)

        page = 1
        try:
            while True:
                print(f"now: {page} | {model} ")
                classModel.log.msg.info(f"Initing scraping on page {page}")

                news_on_page = await classModel.page(f"{classModel.url}{page}")
                if news_on_page:
                    await classModel.posts(news_on_page, model)
                    latest_page = temp_page.page()
                    if page > 2:
                        temp_page.save({page: len(news_on_page)})
                    if page == 2 and latest_page != 1:
                        page = latest_page    
                    page += 1
                else:
                    classModel.log.msg.critical(f"Loop fineshed on page {page}")
                    break
        except Exception as e:
            classModel.log.msg.error(f"Error: {str(e)}")
        finally:
            classModel.log.msg.critical(f"Scraping finished")

def run_in_thread(model):
    asyncio.run(main(model))

if __name__ == "__main__":
    nmodels = ['JornalGrandeBahia','LfNews','VilasMagazine','BurburinhoNews','BahiaNoAr', 'RelataBahia']

    threads = list()
    for model in nmodels:
        thread = threading.Thread(target=run_in_thread, args=(model,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()