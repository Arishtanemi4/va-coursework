import __init__ as init
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap  # pip install umap-learn


def column_rename(df, mapping):
    """Applies the exact same column renaming to the raw 2011 data that preprocess.py applies to the cleaned data"""
    df = df.rename(columns=mapping)
    df = df.rename(columns=init.tableau_snake_case_names)
    return df


def compute_proportions(df):
    normalization_map = init.normalization_map
    df_props = pd.DataFrame(index=df.index)

    for denominator, features in normalization_map.items():
        valid_features = [col for col in features if col in df.columns]
        safe_denominator = df[denominator].replace(0, 1)  # accidental infinity safeguard
        
        for feature in valid_features:
            df_props[feature] = df[feature] / safe_denominator

    return df_props.fillna(0)


def main():
    print("Loading datasets...")
    
    df_2011 = pd.read_csv(f"{init.root_data_output_join_dir}2011.csv")
    df_2011 = column_rename(df_2011, init.census_ethnicity_mapping_2011)
    df_2011['year'] = 2011

    df_2011_on_2021 = pd.read_csv(f"{init.root_data_output_join_dir}2011_on_2021.csv")
    df_2011_on_2021['year'] = 2011

    df_2021 = pd.read_csv(f"{init.root_data_output_join_dir}2021.csv")
    df_2021['year'] = 2021

    df_comparison = pd.concat([df_2011_on_2021, df_2021], ignore_index=True)

    print("Computing proportions...")
    props_2011_orig = compute_proportions(df_2011)
    props_comparison = compute_proportions(df_comparison)

    totals_to_exclude = ['white_total', 'asian_total', 'black_total', 'mixed_total', 'other_total']
    pca_features = [col for col in props_2011_orig.columns if col not in totals_to_exclude]


    print("Processing 2011 Analysis PCA & t-SNE...")
    scaler_2011 = StandardScaler()
    scaled_2011 = scaler_2011.fit_transform(props_2011_orig[pca_features])

    # PCA 
    pca = PCA(n_components=4, random_state=42)
    pca_result = pca.fit_transform(scaled_2011)

    loadings = pd.DataFrame(
        pca.components_.T, columns=['PC1_Weight', 'PC2_Weight', 'PC3_Weight', 'PC4_Weight'],
        index=pca_features 
    )
    loadings.to_csv(f"{init.root_data_output_result_dir}pca_loadings.csv")

    # t-SNE
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    tsne_result = tsne.fit_transform(scaled_2011)

    # Compile Final 2011 File
    props_2011_orig = props_2011_orig.add_suffix('_prop')
    df_final_2011 = pd.concat([df_2011, props_2011_orig], axis=1)
    
    df_final_2011['PCA_1'] = pca_result[:, 0]
    df_final_2011['PCA_2'] = pca_result[:, 1]
    df_final_2011['PCA_3'] = pca_result[:, 2]
    df_final_2011['PCA_4'] = pca_result[:, 3]
    df_final_2011['TSNE_X'] = tsne_result[:, 0]
    df_final_2011['TSNE_Y'] = tsne_result[:, 1]

    # UMAP
    print("Processing Comparison UMAP...")
    scaler_comp = StandardScaler()
    scaled_comp = scaler_comp.fit_transform(props_comparison[pca_features])

    reducer = umap.UMAP(n_components=2, random_state=42)
    umap_result = reducer.fit_transform(scaled_comp)

    props_comparison = props_comparison.add_suffix('_prop')
    df_final_comparison = pd.concat([df_comparison, props_comparison], axis=1)

    df_final_comparison['UMAP_X'] = umap_result[:, 0]
    df_final_comparison['UMAP_Y'] = umap_result[:, 1]

    out_2011 = f"{init.root_data_output_result_dir}2011_analysis.csv"
    out_comparison = f"{init.root_data_output_result_dir}2011_2021_comparison.csv"

    df_final_2011.to_csv(out_2011, index=False)
    df_final_comparison.to_csv(out_comparison, index=False)
    
    print(f"Success! Exported:\n1. {out_2011}\n2. {out_comparison}")

if __name__ == "__main__":
    main()