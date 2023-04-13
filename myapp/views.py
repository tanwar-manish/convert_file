import pandas as pd
from django.shortcuts import render,HttpResponse

def upload_file(request):
    if request.method == 'POST':
        # Get the uploaded file from the request object
        file = request.FILES['file']
        
        # Get the desired file name entered by the user
        filename = request.POST.get('filename', 'modified_file.csv')
        
        # Read the file data into a Pandas DataFrame
        df = pd.read_csv(file)
        
        # Separate the data based on the prefixes
        df1_3 = df[~df['address'].str.startswith('bc')]
        df_bc = df[df['address'].str.startswith('bc')]
        
        # Modify the df1_3 DataFrame if it has any data
        if not df1_3.empty:
            prefix_len = 5
            df1_3['First'] = df1_3['address'].str[:prefix_len]
            df1_3['Last'] = df1_3['address'].str[prefix_len:]
            new = df1_3[['First', 'Last']]
            aaa = new.groupby('First')['Last'].apply(list)
            dff = aaa.to_frame()
            newDf = dff.transpose()
        else:
            newDf = pd.DataFrame()
        
        # Modify the df_bc DataFrame if it has any data
        if not df_bc.empty:
            prefix_len = 8
            df_bc['First'] = df_bc['address'].str[:prefix_len]
            df_bc['Last'] = df_bc['address'].str[prefix_len:]
            new = df_bc[['First', 'Last']]
            aaa = new.groupby('First')['Last'].apply(list)
            dff = aaa.to_frame()
            newDf_bc = dff.transpose()
        else:
            newDf_bc = pd.DataFrame()
        
        # Combine the modified DataFrames into a single DataFrame
        newDf_combined = pd.concat([newDf, newDf_bc])
        
        # Return the modified DataFrame as a CSV file for download
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        newDf_combined.to_csv(path_or_buf=response, sep=',', index=False)
        
        return response
    
    # Render the upload form template if the request method is GET
    return render(request, 'upload_form.html')
