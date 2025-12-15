from pathlib import Path
from owlready2 import get_ontology, sync_reasoner


def print_object_properties(ind):
    print(f"\n=== {ind.name} – Object Properties ===")
    for p in ind.get_properties():
        if "ObjectProperty" in str(p.is_a):
            values = getattr(ind, p.python_name)
            if values:
                print(f"  {p.name} -> {[v.name for v in values]}")


def run_reasoner(input_path: Path, output_path: Path):

    # ---- load ontology and namespaces ----
    # --> uncomment depending on your compatibility needs:

    # onto = get_ontology(f"file://{input_path}").load()    # --> 1 windows: compatible file URI
    onto = get_ontology(input_path.as_uri()).load()        # --> 2 OS: alternative way using as_uri()

    bond = onto.get_namespace("http://example.org/bond/")

    billie = bond.Billie_Eilish
    vesper = bond.Vesper_Lynd

    # ---- start reasoner ----
    with onto:
        sync_reasoner(infer_property_values=True)

    print("\n=== AFTER REASONING ===")
    print_object_properties(billie)
    print_object_properties(vesper)

    # ---- save inferred ontology ----
    onto.save(
        file=str(output_path),
        format="rdfxml"
    )

    print(f"\nInferred ontology saved to: {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent

    input_path = base_dir / "data/triple_store/james_bond_knowledge.owl"
    output_path = base_dir / "data/triple_store/james_bond_knowledge_inferred.owl"

    run_reasoner(input_path, output_path)
