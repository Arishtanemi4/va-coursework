import __init__ as init
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def pre_pca_concat():
    df_2011 = pd.read_csv(f"{init.root_data_clean_joins_dir}2011_cleaned.csv")
    df_2021 = pd.read_csv(f"{init.root_data_clean_joins_dir}2021.csv")

    df_2021 = df_2021.reindex(columns=df_2011.columns)

    df_2011['year'] = 2011
    df_2021['year'] = 2021

    df_master = pd.concat([df_2011, df_2021], ignore_index=True)

    return df_master


def compute_proportions(df):

    normalization_map = init.normalization_map

    df_props = pd.DataFrame(index=df.index)

    # Computes the propertion of sub populations within each ethnicity
    for denominator, features in normalization_map.items():
        valid_features = [col for col in features if col in df.columns]

        safe_denominator = df[denominator].replace(0, 1)  # accidental infinity safeguard
        
        for feature in valid_features:
            df_props[feature] = df[feature] / safe_denominator

    df_props = df_props.fillna(0)

    return df_props


def main():
    df_master = pre_pca_concat()
    
    print("Computing proportions...")
    df_props = compute_proportions(df_master)

    totals_to_exclude = ['white_total', 'asian_total', 'black_total', 'mixed_total', 'other_total']
    
    pca_features = [col for col in df_props.columns if col not in totals_to_exclude]

    print("Scaling features...")
    scaler = StandardScaler()
    
    scaled_features = scaler.fit_transform(df_props[pca_features])
    
    pca = PCA(n_components=4, random_state=42)
    pca_result = pca.fit_transform(scaled_features)
    print(f"Variance captured by PC1, PC2, PC3, and PC4: {pca.explained_variance_ratio_}")
    
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    tsne_result = tsne.fit_transform(scaled_features)

    loadings = pd.DataFrame(
        pca.components_.T,
        columns=['PC1_Weight', 'PC2_Weight', 'PC3_Weight', 'PC4_Weight'],
        index=pca_features 
    )
    loadings.to_csv(f"{init.root_data_clean_joins_dir}pca_loadings.csv")

    df_props = df_props.add_suffix('_prop')

    df_final = pd.concat([df_master, df_props], axis=1)

    df_final['PCA_1'] = pca_result[:, 0]
    df_final['PCA_2'] = pca_result[:, 1]
    df_final['PCA_3'] = pca_result[:, 2]
    df_final['PCA_4'] = pca_result[:, 3]
    df_final['TSNE_X'] = tsne_result[:, 0]
    df_final['TSNE_Y'] = tsne_result[:, 1]

    output_path = f"{init.root_data_clean_joins_dir}tableau_ready.csv"
    df_final.to_csv(output_path, index=False)
    print(f"Saved tableau ready data to {output_path}")


if __name__ == "__main__":
    main()