from app import app
import meinheld

if __name__ == '__main__':
    meinheld.listen(("0.0.0.0", 8000))
    meinheld.run(app)
