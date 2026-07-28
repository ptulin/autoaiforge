import os
import argparse
from huggingface_hub import snapshot_download
from sqlalchemy import create_engine, Column, String, Integer, Table, MetaData
from sqlalchemy.orm import sessionmaker, registry

# Database setup
DATABASE_FILE = "llm_cache_manager.db"
engine = create_engine(f"sqlite:///{DATABASE_FILE}")
metadata = MetaData()

models_table = Table(
    "models",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True, nullable=False),
    Column("version", String, nullable=False),
    Column("path", String, nullable=False),
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)

mapper_registry = registry()

@mapper_registry.mapped
class Model:
    __table__ = models_table

    def __init__(self, id=None, name=None, version=None, path=None):
        self.id = id
        self.name = name
        self.version = version
        self.path = path

def list_local_models():
    """List all locally cached models."""
    session = Session()
    models = session.query(Model).all()
    result = [(model.name, model.version, model.path) for model in models]
    session.close()
    return result

def clean_unused_models():
    """Identify and remove unused models from local cache."""
    session = Session()
    models = session.query(Model).all()
    removed = []
    for model in models:
        if not os.path.exists(model.path):
            session.delete(model)
            removed.append(model.name)
    session.commit()
    session.close()
    return removed

def download_model(model_name, version):
    """Download a specific version of a model and cache it locally."""
    try:
        model_path = snapshot_download(repo_id=model_name, revision=version)
        session = Session()
        session.add(Model(name=model_name, version=version, path=model_path))
        session.commit()
        session.close()
        return model_path
    except Exception as e:
        return str(e)

def main():
    parser = argparse.ArgumentParser(description="LLM Local Cache Manager")
    parser.add_argument("--list", action="store_true", help="List all locally cached models.")
    parser.add_argument("--clean-unused", action="store_true", help="Clean unused models from the cache.")
    parser.add_argument("--download", nargs=2, metavar=("MODEL_NAME", "VERSION"), help="Download a specific model version.")
    args = parser.parse_args()

    if args.list:
        models = list_local_models()
        if models:
            print("Cached models:")
            for name, version, path in models:
                print(f"- {name} (version: {version}, path: {path})")
        else:
            print("No models are currently cached.")

    if args.clean_unused:
        removed = clean_unused_models()
        if removed:
            print("Removed unused models:")
            for name in removed:
                print(f"- {name}")
        else:
            print("No unused models to clean.")

    if args.download:
        model_name, version = args.download
        result = download_model(model_name, version)
        if os.path.exists(result):
            print(f"Model '{model_name}' (version: {version}) downloaded to {result}.")
        else:
            print(f"Failed to download model: {result}")

if __name__ == "__main__":
    main()
