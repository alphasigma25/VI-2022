import pandas as pd

countries = [
    'United States of America',
    'Switzerland',
    'United Kingdom of Great Britain and Northern Ireland',
    'France',
    'Germany',
    'Netherlands',
    'Spain',
    'Italy',
    'Austria',
    'Italy',
    'Canada',
    'Ireland',
    'Sweden',
    'Norway',
    'Australia',
    'Denmark'
]

DevType = [
    'Developer, full-stack',
    'Academic researcher',
    'DevOps specialist',
    'Developer, back-end',
    'Developer, desktop or enterprise applications',
    'Developer, embedded applications or devices',
    'Developer, game or graphics',
    'Developer, front-end',
    'Engineer, data',
    'Developer, QA or test',
    'Developer, mobile',
    'Database administrator',
    'Cloud infrastructure engineer',
    'Data or business analyst',
    'Designer',
    'Marketing or sales professional',
    'Data scientist or machine learning specialist',
    'Security professional',
    'Project manager',
    'Senior Executive (C-Suite, VP, etc.)',
    'Engineering manager',
    'System administrator',
    'Scientist',
    'Product manager',
    'Engineer, site reliability',
    'Educator',
    'Other (please specify):',
    'Blockchain',
    'Student'
]

Employment = [
    'Employed, full-time',
    'Student, full-time',
    'Student, part-time',
    'Not employed, but looking for work',
    'Independent contractor, freelancer, or self-employed',
    'Employed, part-time',
    'Not employed, and not looking for work',
    'Retired',
    'I prefer not to say',
]

EdLevel = [
    "Master",
    "Bachelor",
    'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
    'Some college/university study without earning a degree',
    'Something else',
    'Primary/elementary school',
    'Other doctoral degree (Ph.D., Ed.D., etc.)',
    'Associate degree (A.A., A.S., etc.)',
    'Professional degree (JD, MD, etc.)'
]

Age = [
    #'Under 18 years old',
    '18-24 years old',
    '25-34 years old',
    '35-44 years old',
    '45-54 years old',
    '55-64 years old',
    '65 years or older'
]

def filter_multicat(df : pd.DataFrame, column, filter) -> pd.DataFrame:
    return df[df[column].str.contains(filter)]

# ------------------------------ techs ----------------------------------
tech_selected_columns = [
    # inputs
    'EdLevel','DevType','Employment','Age',
    # outputs
    'CompTotal',
    'YearsCodePro',
    'LanguageHaveWorkedWith',
    'DatabaseHaveWorkedWith',
    'PlatformHaveWorkedWith',
    'WebframeHaveWorkedWith',
    'MiscTechHaveWorkedWith',
    'ToolsTechHaveWorkedWith',
    'NEWCollabToolsHaveWorkedWith',
]

tech_values = {'LanguageHaveWorkedWith': ['JavaScript', 'TypeScript', 'C#', 'Cpp', 'HTML/CSS', 'Python', 'SQL', 'Swift', 'Lua', 'PHP', 'C', 'Java', 'Delphi', 'Bash/Shell', 'PowerShell', 'Rust', 'Elixir', 'Erlang', 'Ruby', 'R', 'Scala', 'VBA', 'Dart', 'Go', 'Kotlin', 'Groovy', 'MATLAB', 'Perl', 'Haskell', 'Julia', 'LISP', 'Assembly', 'F#', 'Clojure', 'APL', 'Crystal', 'Fortran', 'Objective-C', 'SAS', 'OCaml', 'Solidity', 'COBOL'],
 'DatabaseHaveWorkedWith': ['Microsoft SQL Server', 'Cloud Firestore', 'Elasticsearch', 'Firebase Realtime Database', 'MongoDB', 'MySQL', 'Couchbase', 'CouchDB', 'PostgreSQL', 'Redis', 'DynamoDB', 'Neo4j', 'SQLite', 'Cassandra', 'MariaDB', 'Oracle', 'IBM DB2'],
 'PlatformHaveWorkedWith': ['Firebase',
  'Microsoft Azure',
  'AWS',
  'Google Cloud',
  'Heroku',
  'DigitalOcean',
  'VMware',
  'OVH',
  'Linode',
  'Managed Hosting',
  'IBM Cloud or Watson',
  'Oracle Cloud Infrastructure',
  'OpenStack',
  'Colocation'],
 'WebframeHaveWorkedWith': ['Angular.js',
  'ASP.NET',
  'ASP.NET Core ',
  'Angular',
  'jQuery',
  'Node.js',
  'Next.js',
  'React.js',
  'Svelte',
  'Vue.js',
  'Express',
  'Phoenix',
  'Ruby on Rails',
  'Django',
  'Flask',
  'Laravel',
  'FastAPI',
  'Gatsby',
  'Nuxt.js',
  'Drupal',
  'Symfony',
  'Blazor',
  'Fastify',
  'Deno',
  'Play Framework'],
 'MiscTechHaveWorkedWith': ['Pandas',
  '.NET',
  'Keras',
  'NumPy',
  'Scikit-learn',
  'TensorFlow',
  'Torch/PyTorch',
  'Hugging Face Transformers',
  'Apache Kafka',
  'Apache Spark',
  'Tidyverse',
  'Electron',
  'React Native',
  'Spring',
  'Flutter',
  'Qt',
  'Xamarin',
  'Capacitor',
  'Cordova',
  'Ionic',
  'Hadoop',
  'GTK',
  'Uno Platform'],
 'ToolsTechHaveWorkedWith': ['npm',
  'Homebrew',
  'Docker',
  'Terraform',
  'Kubernetes',
  'Yarn',
  'Ansible',
  'Unity 3D',
  'Puppet',
  'Flow',
  'Unreal Engine',
  'Chef',
  'Pulumi'],
 'NEWCollabToolsHaveWorkedWith': ['Notepad++',
  'Visual Studio',
  'Visual Studio Code',
  'Xcode',
  'Atom',
  'IntelliJ',
  'PyCharm',
  'Sublime Text',
  'CLion',
  'Eclipse',
  'Emacs',
  'Android Studio',
  'RAD Studio (Delphi, C++ Builder)',
  'Rider',
  'IPython/Jupyter',
  'Neovim',
  'Vim',
  'Nano',
  'RStudio',
  'NetBeans',
  'PhpStorm',
  'Webstorm',
  'GoLand',
  'RubyMine',
  'Spyder',
  'Qt Creator',
  'TextMate']}

def aggregate_techs(data, outputName):
    output = {'techs':tech_values[outputName], 'CompTotal':[], 'YearsCodePro':[], 'Number':[] }
    for tech_type in output['techs']:
        df = filter_multicat(data, outputName, tech_type)
        output['CompTotal'].append(df['CompTotal'].mean())
        output['YearsCodePro'].append(df['YearsCodePro'].mean())
        output['Number'].append(len(df))
    return pd.DataFrame(output)

def getTechOutput(data, devType, edLevel, employment, age, outputName):
    df = data
    df = filter_multicat(df,'DevType',devType)
    df = filter_multicat(df,'EdLevel',edLevel)
    df = filter_multicat(df,'Employment',employment)
    df = filter_multicat(df,'Age', age)
    # il faut calculer salaire moyen et nb années exp moyen
    return aggregate_techs(df, outputName)