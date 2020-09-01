# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/23 15:39
# IDE：PyCharm
from Tools.functions import *
from Features.rematch_feature_name import *
import os

HighRiskOppositeNoM = ['8a2997e892d3df65356aa6f66e64eb83b8866c11d96886eb47a30c286a79dc1b3636b6c3a865865824a583ac1b00b169cdf67c6613866b095d59cc20fbdd1b12', '6e7783ae2975bda17ccddcaf3199431589f51e33a05096da5ead9d69107a919f8f39486589445d3bf8ef69d9df0a55a613396c5eec51b156713c55ae17840e74', '4b588983e45d1e4df587936878cafda184fa9760f4815a7edff401ac9745e2e08ab2fa7fa8eb9c798693fc1322c0740a619dc524fc5fadbd72de9d69fcad84d9', 'ad79f63e6ef91690cb9e0c69d9104e2fc412df2193650c44adada2e0f1128999f9473385034b1cd1a84909ff02b6e4d82ae5d16515b8c437cbfb1f3ae49fb2a5', '47f9170d4f00af02b40e122fdd1e1cac24793d8309cbe2aa6a30c491d1fe4a461baff4fc05c07b49edc76267587c783af5812ff21cf7c4ad17f8c0cce6c80953', '96ca6908b78f047e488bcacfa99afc1915b1db625cdc8f40bee9c73e8474b3e970db03ee371fbea26aff226dbc8f1b05c5224093026ed1692d767b81fb331307', '11e765b002180dbbf61beb49280241eccf71654f34d52410e15bab0d0caaf0a7fbbfed2e2f9a2df0bb9ff89f086e9a223109966e3c60c774c7028e81f7d8f712', '494c643e95920626de35b7cd377ad55d031c1309a128d11589aa429d34d1db46d80f9d481c7054401ff90d6f9d40b5062e382ed2a16cb594bace41a278895cba', 'ac83116ed923b92c53401b016d9166c5915377c43c2f5dfb1b6ffb12bca89e37d7aef6be934e3b62889a559eb195ecce04c44f6b89f96566ce65034b87f75a82', '4f3e888c5ec488e84dfa93358e56cb23b8c25f15c9b34727b3d46030f60b2e2229979f9a6ae19af9453037a6d28afdd10e8c49ef863355ddbb7a0c806f6c66d9', '5cde1fc9e3e0ba78896c7da0bc38aa4bb30a6006071dc5d27fec12bd1a81a6a46901095f7d5ddcc3469325c800434e11bcc5fdbb4d3e9f8147bd63c0eda3f201', '9657b1990c2e8fde5a2a16f20d7a2a9f512e073744e110578d7cd234742420d18ca91077a1e3748525898efddae327f8e220df619a6628bb63aa2df6edc435e8', '0f74bab77e4fa353814f99f02420980f9c4a8b078cb38fe2e626a837718afd06bc66eac24267bfb3cc640e0569869d702d172895a34b3b99d7721b5f1ec26de8', '0afca9e78dbc693cd3215b277d06de0b7e29702545f4bb9155e3826cb3bf56e0b9b6a9e311acbeb2b37526b6ca20f78b90cfd321268b65c3a371b598ad0cd278', '1467e1e31d851100923c186e2eadda098b06e6158bc985e895e41b6370c159f5953d7154499326f5afbf4edc27ea941450cb17937a66e22dfc247c4da80be82a', 'c2bdef657b3a4e58ba42a0976c4661cdc467f6248cda179d1856553e7576fa4dadec4617cb4592bbc41972cdde179bac8795a69351c55edcae4bf82025fa7ef4', '88fc6383b0e6217efe95b0bbfbae26bb6a89c96ac980e9e48ba846f72ba061ca493372168d8172511049a536f2109ddf2d6c37a94f459f1b4e318ec80204e742', 'daf72fc1c37704ce5e19e84922eae413c566dff0446edde103d0fd0ef3e9513469b20cdb972533c6fd76f1826fe8f3db0f049e4167d665004847f2350b3dc8de', '8757f67069283bb9e91f9fce110fa2caa2bcf7d714926feb12147d308c4c86a01455fb2947fa7993bf14e57cb5f0b7c6ceb7e290b53e05a6fd429e61181437c6', '08c61513445a5cecd5f95518e927154153f101feed0c77034419b2ce77a5a9558f10d798d8f28b5c2f2d497c8ae35c77c6ee4422feb5fcb7e7738c4ad1986ae4', 'e172d7e57257e3769a20453a507da3f2d681f30eda133753f265c80d68e57a4ab86c683f09bf83550c788ff05fab4873fe68be8997c446058e1273082ff97f23', '3ee20d48b865574fc4e2492c675a4b1feb8d99ce4eb6facf191d7ef454b0cffce79bac11f28bc993c593bbe59fac513e36e7b003869195833ed746a9145c0ae1', '1a99a087d033e16dc63d123075aa309b8b4a9e929fd13a6e29637aa4f5e60b8c7faacc4fe5c65b09802cf904c9cfe8f1259aa13d7d0a8c67b364699bc13f6066', 'e965fbe16b02a55aec9a964c0dc984c85b58a0353b0a82740348fa468d07cf9c10d23f1336b8211978770ba7e3eeda6fcfd73c773df56329741abaf23e453336', 'a8c248a6985a70b4a6e8d633ecca0ba7b3608937452981aad5208d05fb046e3366dbf08d02e5fec23e4a01a75c8ae4f8bf9bd1cc8b680ff865558c524c4121e6', '005dc4be96da7c3554f07336e526b76b9d050b96d23bbdcf2ccdd8fa021098fac0159f5522ffc3b510189d323fd7a08f050e12952e6b0cf9fc61e6f3d3bd29bf', '7a8c8ae5b681e16dee5d582f8c8427d2b91e7c4622469ec277fd9fcfe4a584ce17bf622780adbc693843f6e3e2b8c04f19ddcd94cac9379127ea138920c7ea34', '258271e8a99969f77a1f76ca6bf3df08b3f3c2a74ad5a7e22c248e8207a18d1fcaafee50051ceae6b68bc9867a074512978775fc2daf73ad444dc6319273f5af', '54288488f0976c3066ba118fc3fc50c8dc39a89af91f3fbfd190bf29184b12aa126170f70bbcfff78c84d0f9858d15dfa7a29b4cb214782703217b7b47b0eb01', 'cc6719600b602ab3dc631629de00cad867efbb5f857cc3b912e81e060a96a51dcee2ce4b954e59278be019642d3f6a458676d1ab3882ababc87dab53c2368283', 'fbc73b5cc6ec34ffad793fdbc716775ec5c7d913ad8718e1530facbb655649b1176414e3be2777e4b81f15fe41af41a1ed3aafccab9e9013b4e676b535a0f440', 'e516bd56308ce3309e806892b5a5aa68365b032bd032d839a9740ff387b756e00bc78be3626fbd0534a393c5d72ba348c330070b4e9faa46a3c4958a147b43b8', '2c63614010c0b16a0fc0e968325d97e53ef4c6b01ef42b36aa9dfb50675b94e6f56a755917e1fd71a98fba5bca95d6adcf515e1b9ef1c5f7821f27e9d7da7bc6', '55d01b3b2eac9e9a8d16d4732930094ac8688fac2e9f09af82921bcc01f106b3486a687f92b30a1577069dec2ac6fa999188764a6ee36fa4fcffdceb7e8dddb1', 'b18b32ff0286e3be0a99e3b067819118c20d2b89c197f3703fc1b48b649626d292d7b69a84e7a74f23c3f5ab9d5378d0599e4675a02d3dc752b7084862e5f2ed', '54186a6512ae270fd997d701956374008ed7ea9d8e55fa88d3ffb71dab9b86e3e271adc6db6b96639e9c08c302cc2ac89ea6755808bf4100a9b8cc0ebe3162af', '37466030fdf6672ff0b2fccd861967e680cfffab7e021503bd82970d36ecff59354e0751388e1aa0609e967cae30617c52715c1fa7db2e5de16972bd4d5983e2', 'c20eb97f4cd8260193f04ba5d8e212f53c28baa22833fb8e534868a31af585d49782b669f8182b8e3893b528f8ceec2e4a5e520c53e2dd279f53a474c8b428e8', '386ea50b35dc1d516ba6eea2f0760b107facc9109dfa43e12cbdd953eaf2d8674733c562d8728764f2e3c0c83854727b3eacf702b6b140789ff74b13f0345b50', '3934a22ae36dadcd15bdd2f7f01952bdb5695c6f57fb5763b582dc376d7567c85ae2e73ccd6398e4539d7ae7b3281c6c70e9ecebb4fbdaad652e1e009a15b0a4', '2359e0e13b95fae1a7fb2f06391beda54c32a56e514fa4a1d78315e7592898597f5dac7cf66c465b9ac21a696173026356e5e94abe1755b8ccab353ff48117a2', '8dddce008590c6bd7aa252c27170e6bdddc74b615c2a6d93a94b3afabc1fc7c1cb1e534fd4106a3a9b1ac65028cddd2c4eef6011668b08fb8b05803e03796818', '29b004b4d7034f32bb0c59b0439db4dc40e4cee737836769dbb66c3a7db807b007da6f2939a67a6f2d07d9a2c619fcfda8d6090a057e82121f5aef5c971fdef0', 'b590bebfa815f6c4ff79e017f431ac50f0ee7f098e91896f788231a0b03d7862d548136b92245418c9cf0b82656aaaa317856c4eb54ecc9965b4cd6c4b04bb56', 'fb49d7aad605001cb0969ff7a9d45867692c63192f819589fb7c149649471a7d9e2823cb4c8372dffdb64151b3af0ef5b7d4617948b8a1a6aba78943447de0e7', 'bf13b7c6145bedcec5d16e337c31fcec59f7e1c54bb98a6b80b54e42dd2015ca3703187ba3fa0b2649518e12e538b4b9f6d599acf2551055974a398eadef9a5a', 'dd72c3a6ef62edd45ce8f085fa067ea54d28552a1d4bdffd2fe3cf9a64ead53332e398c2410e0f9e8530450a8c1434d6d0d6a520cf60c3e82074753a5c025d58', '13c0070c4bae75cc8c1f69bb54d8c64686cb176346f03972bc689ca7cc85c717d652f7ded497d83b54b9f85ef985f0fd0fa57f2a158318a6742e09cf0c8669f6', '0f8cd6d7556f6bbccf87bbfe80117534be8a308f068c67558ee19a1d8b2e3c45817eb1b72301419ca2e68416d1ceadb99b6cb52cc39f5a019d4d2b7f4f7709dd', '6997ef05c8a1402b9d66dc61bf1c5efc4d1d7addfa44857777fbb72ed54552aa0893ccbfba932b47c94311c7f7e20569aff004264087679ef1fd312df08cebe8', '4f350621c651820c3cb5d1a0b7a88424a97422360b8c2f12ca3cdc2da2635914df94a69821a323ea9d6070ec1d23962df1a3692b653a8bf1eac8358300e3761f', '8048b4e1e03b364a672919319b48f3b911bd5464f018eeab2542af55f46d179a02f956cfad32c95f8aa9c03f83f5e21136df2006bb271074d83fc2ec3da403f8', 'a6d89378d958b3bc0911a58701ec7d38a3036fb0313fdbf0757208a32c4d432cef5028ec99de4dfafc8d0abc5ea3858c4cb7e2483d364e144f1fd78664d41f8a', '179325d88f5784c10203dce3ca868b3ca4802f3740e6d2686da76ee12d9adc98a1a20c16202bfafcaed0cdcaa1ac88482b65014a4b6d3d26a3ce2c90a4874d06', '293a668f95c6381522529b05a3e7e8e676818d28b98022d04c52f49af2398b5ce3b3819a0382ed06d4ead4fae22983a735376fac27a9ad4e53fdf99040eb54f0', 'c8e3ca69cc706893d8a1f3c63ffd58ab990c09a337acf96be44924a6861414ef848520f5e1994fb0485b0a7c08d0a456f4daf3203de4845cb999656c82c1c695', 'f2ed12119ce4139530f20fead464bd11ac3e293f71432f1718d615d8bc1af09a4d675f2722bd877f24383640f203437f30045fdabf0cb7f05cca7169edc8ef0e', 'f00125af0d880a0679f948cef5ddaca38e6bdec9d1bf4148d0fc4bb8d73e260491223938943e5829ec175a11e3f986c830824600e1bfdda54fc9631ea9055314', '6616392d7abf8bd784e8689fc193287b97e9897e35ab433a832aea5812a8f4f42ff8cc9844f47dc0d94b881b48868c9a64c35f6d0e4d5cd0d425582e6ce1255d', '10d4db2cc42d6e6c5f64370c3e3b26ef30bb1a8e7cbae92d6e6f9363f4d59d7f7d70d0e6052bb7c4038a03d0579fbe9a1c5c5799f46eabaf478caf191b508473', 'c1913042dddad8adff7e4ca15f9726b7cf72d2a6a003ac6e0f9e80c193f6d0f92ccd9584990343e0cebc0b7f40841f2ba058749164a8bb2a93cc69f23f8d1aec', '5a5c0fa38c956756f8c38ff7bcf36ff87f5f92aa777f94a26f135fe513d30c0c258aac7ea8680eb4daea1d8e592c2df3c8485aa2e06c0cca70e48df36e615766', '4655460d5d55dd6c8e623eaf75ccea47154c7752b6f7d18d914abcd8cd4f6a7338f358bab2240219d809fdc470831d86684a89dd74da11cf265dfe47833114e0', '9d1d789beead75bbff1c2db929e1a5074a244c10753cf2a13fe7342dc589db3092edaaff36a34a74d3c4b4affff65cdaba70e47d8b476033a71713c119b5ce3c', '0614029be58eacae48030b24aafc5d1adda4cfa5130e95c326316acffc8edb9a11f1c5276e3556122085ae14aa6abeb6708c0ad7de6079277197e41ad4f99519', '7017a9f23754b29f72c308553c4b1b18493ff1bd03946edc9687e3a8f1c1893b7f9391dce6809d6fba24d199cbe4ffa6fe65ddcbcb6e7aedfde0b8245091ba2d', '9911288358ae6bde64a5271f71404e89b2f6fe13728dc779b3adfeea897722b4af1b228323bc95aae4075376777ec466172e5b16844e8eef676e75e7e2b3b357', '61f5b973f56e087260a880deb9c32528efd29e5525c5d25fb970aebab3982559087dc35434942af9e6b6cf181bf5751cada89754493def9326fd5e2d2c2469a9', '4691989526ec56fd1050837928b88f88a9c042693ae720c658c013533b26faf45135c98062d2d791587d1ef1b93e0a1bd1c6bef3402f388047a292afbde74de9', '173e81c9c2aaa6dfa06a9ac9a370026c52a83c1c88d3f1bc77dbf41b9a09a1f0b793274e35d37f26015fd0bd4ffba3722be1f07d30a1e02c5651b889b51b6491', '1ab3aa200b833ced5dc89f4fe79795be64a82ab9bb2e6aa434abc28002d4a67ab97c878fc24c7579f58884a30a9e9c6f5b4e36d19f3506d079690618bffc5a47', '61e86e0dd5170ace971f266a3af830d477177231e43545c911ba42e2a72f7cceb98e96837f6afdaf8f53090728e87a64b0dc98e30a08c7a58b5f53bec09dfbda', 'b48a4fabaafb6a85fc6f3c5e362b616bdbf6e55faffa405963942a8b442f13e1dea62badc49e43ae7dbee6eeb2a1c23620562c5992fe878447c7c1d5e6b34090', '16160044598aabb7628fab22b0b2ad970103ec5f9bd07ef4fc16de04be0c2a4ae8390fda11973cefe559b8ae580276f0ae8e5241e5d3ae29a89ce8b261dac3bc', '0ded27d8978b309384510d17e0ed58ffaf2897292a723e64681a5740f867574928cdf3bde52569721950875d589c47decbdaa0878d44f6101f1a2abe07948f51', '4d122bc0d459300dc6a5f77eeda7fc2ee4eeaba31101467fe1fd53a6474e4d6e61bcbe6965487f75a1f4c30780ebcc9a8eee17a74195c9340a701bd3ba5a2842', 'e8a15529cd99afb1b169ffcbfb5d5e7b2e4064904931f647d69fa6ef3b8f2d6b179d36525733e2594b0c284fedc82577bdac4b8ea52acd92035e43ff18d069a3', '6e7aa2914bb8ed3c0474b851e2ce634a2e86ca52f80cf2bfc28b158e75aa07a3268d20dbb42c0324e33f1eac8ebd15e53fe3aeaeb2a3f30cd184aa296d30432e', '5d33626c79731eec2af7519f948c6fd546cc6c961309d9a02a077827221cb6a8b5795734fbf96977102d1119d3bbfa346ae423b6ff88cc27b5a1a9dfe3dc7921', 'aff18edefa5c584259d3ddf376225e885d66fa67708ff385a54b3720ac098fd01bf5d317de79ac0caacf932543acdb3124b198df1b3e6776ae0b8750e9cc5a2b', 'be846c1cc18b02abb82aa9df38c49fb841d516bb251009db09f147c13a3f445ac316d37bbb74704094e3b340e60bcc7b7dfae3113657fab458f7b1f0cc237458', 'd920be310303fb83534717b05f1789c77d65ee5ecc6e44c0713549f10e27b011543e9f3ae55afa4b39a33449de42094e3474e67aaa409b91ccfbf095f13d124d', 'a64da8caea708ecb7492ab92dd3f75ac3079fce3574cddf9273aff2df2ef3164898dcc432503af4c6f88318951b48467a1e3538fad20f340e8cba19e9d37e76e', '726c630546cbd20da2e9d743aa92e5419db4f91217935eac85cd5d139900f2433fcab49c4e507df4f99f0601a0f4cc13a5b4d5c1aa6fffa0cf3d680676fb4f65', '841a7c4ca8e0f3f7be4ab8d04d91b4502230cf16782d69c82458cbc2264887be453abe697c69218b429651ba52e1bfebe96ff912c3cda4839d87632fd32ad510', '708600ab0f9648b772f8490919dfe1f9e2096aa72d911dbf4d801fb8c6ff1dda694722d3b724431e3f4fe8755cdcfba6d9ce29cd52effe87e913a15e6b1d1dfc', '617682a7caf42c0e2d1785577751329cdbdce997698f65aa0887fa81f68581387a2b75667746d76d5da918596b23ad632a72184c68cc8ccaf002a14c35913bce', '25de4375f7c9c1aa3221e3b8d06142cc83dac8c0bd71423a4b198d59f18d84cdbd8456e5c358a712cab4e9ccc9cf3ffd3a9fe6930eaf5a74fa74ebfd9f11f1a0', '94774aecef892c1635811fbb478f7f420921a15fdbfb6846f5da8341748a96b87ee5ab3f27deb136f0ced24a3c3435bfe18064e2db2465185747faffb2476c55', '3cc1cda2e7ac2334166dbfd7d35fdbb6c38904aaeff656d6eb3c1a46491067bcf8f7f24c5cfde6a0cbf93dbe9ac5d5379b3b3c1328eae59f74e43ace53916b61', 'a9bf752040a4c28738f765af6b3fc28c0376c88215f848d9609ebbf71b44315da000350329b7acd4cf3e001f66cebba23dcda9f858a21b457a9c159c7a985742', 'ee78ffe1c82608a0a2ce4476be62a28b87e0bce6f1b7ed3991d1b0eeede4e36db36378d83c515494bec819b8b3d2f7dff700ae25cd7f408622a589775847edf2', 'b78942aff4c96415455bff1503d606c66bbf5935f0d7a6a0fc790f1012da8dd0b3dce754723931556d6e95fb039d909ad35780b25bdaf1c01f10325d31b10d6c', 'd0729fcfade04f099605de3d8ece962b556c48ec99f1c4ccabeb0ac281fb8448433e2d1546ed66903c245a03c555125dda168030bff31670917135ba976af673', '99d25be6264445f745d7a8bcd9601a8802d4437723b7c7ad219fd58684de7d5f54023fcb86d35a9856b28eb1c022af2b3803f1ed56b1f357dfa1b9b8c4bc6cf2', '2666153d4fa3250d235b465284b7833ec2a77731baff933b5b6d0c27ed178bd2efafedf131ee71aa571f29a415f8544b6092e252ce140ec0b9c6c5527b540810', '49b5b3f1ecf7af34527d164d886b9474b0bf33786ce21d52b8dd227975c1e7e1d0aea374fa83b1a8835ae3949e96d1a384979edbfd875f3cd6cc26020f9e78ee', '7fdd5f69b1448116339e9e502e52e9bc0a4ea81a892bd4730ea9ef904aff135d49191987a49ee6d4b57e630b2249d54e6758b7746bc6ac286779695d7fcb0be0', '45800df319cfc8a5563b357230e2d3791813276f971dc53def645d473d2793d55d4a24b426f957a5c71fa14362668dea1ff45e62fac5f4479b7c1adee88d05a9', '12887dd653da32f58ed628dd97edfe42ba61d97dcc94275f3e1e61581a75f2353daaefb62ff7abf6c827ba089a7e4dfb18a3d0e0143f74c03446b8907fa5db26', '7945cad73651bbebfc2ffa31aba40f1bf551ce7130c781cccead1f08f497284effac8a89801a2a29fcea5d6a97d07dcfd7c8f35d6133876a61e71788a0bc9b0d', 'f761afd0fac55db695778e9df887e77ee30488789e599dfb37641df5f0d55cb0b9999538a8bcbf5671e5839c098c5f0f1d303fe902d420d66239b0aa8c370d95', '54bb3b85b4f8679c47ca5c82c53a6bd7e78a7d0d7bd1e04ee85af20cadc5e18e416b95557e00efd275ccb176323a0972ea88b39ecf17b610aef2729d470ded2f', 'ccb14b60a9e9ef77ee8cd533630b518684eb054538793731629a579b49ee46206c12a7f6d1135cb5ec654bdd43e4aab91c699264ee4a587f814aac0432b32cc7', 'c3cdc11e2e9b24046d2e81ab2e50a58453d5d6b2b689328e9f5fc5ddb84c13427ae9125108e5d21212f9591942c36a368f3cb319b51e575542286ad387c35f09', '0c73c3617cd6803e0630b7956853e0ab83cc886bd084c8157314093b7bcf0c94eddea86ad7bcdf916d9940bd3650161efca6917e0a70e8c88292bff55e4a4af7', 'f84ea608af04655dcc0634bf1ed74d839dc4c76fb867fabb38708bcb86c7df5952f2b6d94013af24ebea9a755066c870848d01a95064ce2428936ed8a4a6b503', '73a6c0b943a3b87fe237b53ddfe6b064f196a4a1c4ccbec21061b449cc694b55f1e0581a365be81627e8aabcd13ccb5fc5f1a23cce0be3cbc450ba8f6c4f4972', '00eed0a80d947efbc192a6238e2d4e2565249f09c724f88158783fae7472131154b4c71a40c331a39ab76a0b475da168d019513e30ff03ffb60a06511bb0caf6', 'ed4a784afde0eaac66802bebfa90d23aaacb2d076e2a985f6b1c12ac8ecded182b1b41fbbfd0943e02567e193a1170b3d9dc64266aebcf15468235586f6f032b', 'f6d4b17e35daa91bfaa68aae45d727b249855da77eb8372d10772053545bccbd8a1c3761c27339e37221f940aeda6ffae6bde2207cd9784289ee04319fd81537', '777e81b7e48e5cebf11bde07500dffe10a03b849f0ca745de82450a3bf29e22c2b25249f17798e1aebcf6dd10bce64b14697e6a9a89dca5495fb164ef06e8475', '28f3337330536711ef4e56992e7c6609a69b88f89c2a6cab147da0068897350616b86ed769bc45afe2bde04cf3cf17bdf21f3c30526e0f4095c50bbf83ff5194', 'd4fcf057e00f39b699b4920346f8c089accbc3224db0ee22579c94f67df8e0e4a94dedde81cf348d1916f25f48c3df0b5864bd0f7a8abec6738f5369b5376bcc', '77d1ca482a4499b9e65a82ed3c33a92c72c36d561fa848d3512e1a972780a9ad6bf404f7939444427d1102bb6368f76cb2c2fee0c2d962ceb2fc80d582e67298']


class RematchConfig(object):
    DATA_FILE_PATH = "Data/rematch"

    DATA_TRAIN_USER = DATA_FILE_PATH+"/train_user.xlsx"
    DATA_TRAIN_VOC = DATA_FILE_PATH + "/train_voc.csv"
    DATA_TRAIN_SMS = DATA_FILE_PATH + "/train_sms.csv"
    DATA_TRAIN_APP = DATA_FILE_PATH + "/train_app.csv"

    DATA_TEST_USER = DATA_FILE_PATH + "/test_user.csv"
    DATA_TEST_VOC = DATA_FILE_PATH + "/test_voc.csv"
    DATA_TEST_SMS = DATA_FILE_PATH + "/test_sms.csv"
    DATA_TEST_APP = DATA_FILE_PATH + "/test_app.csv"

    DATA_TRAIN = "data_train.xlsx"
    DATA_TEST = "data_test.xlsx"

    # 加载必要的基础数据
    def __init__(self, is_train=True):
        self.is_train = is_train
        text_to_print = "正在加载训练数据" if is_train else "正在加载测试数据"
        print(text_to_print)
        self.column_name = ColumnName()

        self.user = pd.read_excel(self.DATA_TRAIN_USER) if is_train else pd.read_csv(self.DATA_TEST_USER)
        self.voc = pd.read_csv(self.DATA_TRAIN_VOC) if is_train else pd.read_csv(self.DATA_TEST_VOC)
        self.app = pd.read_csv(self.DATA_TRAIN_APP) if is_train else pd.read_csv(self.DATA_TEST_APP)
        self.sms = pd.read_csv(self.DATA_TRAIN_SMS) if is_train else pd.read_csv(self.DATA_TEST_SMS)

        # self.user = self.user.drop_dupliactes()
        print("正在去除重复数据")
        self.voc = self.voc.drop_duplicates(subset=["phone_no_m", "opposite_no_m", "calltype_id", "start_datetime"], keep="first")
        self.app = self.app.groupby(["phone_no_m", "busi_name"]).agg(flow=("flow", pd.Series.sum)).reset_index()
        self.sms = self.sms.drop_duplicates(subset=["phone_no_m", "opposite_no_m", "calltype_id", "request_datetime"], keep="first")

        if not self.is_train:
            self.user.columns = ["phone_no_m", "city_name", "county_name", "idcard_cnt", "arpu"]
            self.user["label"] = [0] * len(self.user)

        self.data = self.user[["phone_no_m", "label", "arpu", "idcard_cnt"]]

        data_path = self.DATA_TRAIN if self.is_train else self.DATA_TEST
        if os.path.exists(data_path):
            self.data = pd.read_excel(data_path, header=0)

    # 除法相关的运算
    def division(self, numerator, denominator, column_name):
        self.data[column_name] = self.data.apply(
            lambda x: x[numerator] / x[denominator] if x[denominator] > 0 else 0, axis=1)

    # 将新加工的数据data添加到已有的数据库中
    def add_to_data(self, data, column_name, replace_nan_value=0):
        data.columns = column_name
        self.data = self.data.join(data, on=["phone_no_m"]).fillna(replace_nan_value)
        if len(column_name)==1 and column_name[0]:
            self.print_correlation(column_name[0])

    # 对应通话类型的通话记录部分数据
    def get_single_voc_data(self, column_name, call_type_id=0):
        temp_data = self.voc[self.voc["calltype_id"] == call_type_id].copy() if call_type_id > 0 else self.voc.copy()
        temp_data.dropna(subset=[column_name], inplace=True)
        return temp_data[["phone_no_m", column_name]].copy()

    # 对应短信类型的短信记录部分数据
    def get_single_sms_data(self, column_name, call_type_id=0):
        temp_data = self.sms[
            self.sms["calltype_id"] == call_type_id].copy() if call_type_id > 0 else self.sms
        temp_data.dropna(subset=[column_name], inplace=True)
        return temp_data[["phone_no_m", column_name]].copy()

    # 打印皮尔森相关系数
    def print_correlation(self, column_name):
        print("------相关系数为："+str(round(self.data[[column_name, "label"]].corr().loc[column_name, "label"],3)))

    # 通话记录中出现的城市数量
    def voc_city_cnt(self):
        column_name = "voc_city_cnt"
        self.voc_type_city_cnt(column_name, "---正在统计用户通话记录中出现的城市数量")
        return self.data[["phone_no_m", column_name]]

    # 主动拨打电话记录中出现的城市数量
    def initiative_voc_city_cnt(self):
        column_name = "initiative_voc_city_cnt"
        self.voc_type_city_cnt(column_name, "---正在统计用户主动拨打电话记录中出现的城市数量", call_type_id=1)
        return self.data[["phone_no_m", column_name]]

    # 被动接听电话记录中出现的城市数量
    def passive_voc_city_cnt(self):
        column_name = "passive_voc_city_cnt"
        self.voc_type_city_cnt(column_name, "---正在统计用户被动接听电话记录中出现的城市数量", call_type_id=2)
        return self.data[["phone_no_m", column_name]]

    # 呼转电话记录中出现的城市数量
    def turn_voc_city_cnt(self):
        column_name = "turn_voc_city_cnt"
        self.voc_type_city_cnt(column_name, "---正在统计用户呼转电话记录中出现的城市数量", call_type_id=3)
        return self.data[["phone_no_m", column_name]]

    # 通话记录中出现的城市数量
    def voc_type_city_cnt(self, column_name, text, call_type_id=0):
        if column_name not in self.data.columns:
            print(text)
            temp_data = func_count_distinct(self.get_single_voc_data("city_name", call_type_id=call_type_id),
                                            "phone_no_m", "city_name")
            self.add_to_data(temp_data, [column_name])

    # 消耗流量
    def flow(self):
        column_name = "flow"
        if column_name not in self.data.columns:
            print("---正在统计用户消费流量数")
            temp_data = func_sum(self.app.dropna(subset=["flow"])[["phone_no_m", "flow"]].copy(),
                                 "phone_no_m", "flow")
            self.add_to_data(temp_data, [column_name])
        return self.data[["phone_no_m", column_name]].copy()

    # APP数量
    def app_cnt(self):
        column_name = "app_cnt"
        if column_name not in self.data.columns:
            print("---正在统计用户APP数量")
            temp_data = func_count_distinct(self.app.dropna(subset=["busi_name"])[["phone_no_m", "busi_name"]].copy(),
                                            "phone_no_m", "busi_name")
            self.add_to_data(temp_data, [column_name])
        return self.data[["phone_no_m", column_name]].copy()

    # 主动发送短信占比
    def initiative_sms_ratio(self):
        column_name = "initiative_sms_ratio"
        if column_name not in self.data.columns:
            print("---正在加工主动发送短信记录占比")
            self.sms_cnt()
            self.initiative_voc_call_cnt(is_call=False)
            self.division("initiative_sms_cnt", "sms_cnt", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 被动发送短信占比
    def passive_sms_ratio(self):
        column_name = "passive_sms_ratio"
        if column_name not in self.data.columns:
            print("---正在加工被动接收短信记录占比")
            self.sms_cnt()
            self.passive_voc_call_cnt(is_call=False)
            self.division("passive_sms_cnt", "sms_cnt", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 短信记录条数
    def sms_cnt(self):
        self.voc_call_cnt(is_call=False)
        return self.data[["phone_no_m", "sms_cnt"]]

    # 主动发送短信记录条数
    def initiative_sms_cnt(self):
        self.initiative_voc_call_cnt(is_call=False)
        return self.data[["phone_no_m", "initiative_sms_cnt"]]

    # 被动接受短信记录条数
    def passive_sms_cnt(self):
        self.passive_voc_call_cnt(is_call=False)
        return self.data[["phone_no_m", "passive_sms_cnt"]]

    # 主动通话记录占比
    def initiative_voc_ratio(self):
        column_name = "initiative_voc_ratio"
        if column_name not in self.data.columns:
            print("---正在加工主动通话记录占比")
            self.voc_call_cnt()
            self.initiative_voc_call_cnt()
            self.division("initiative_voc_call_cnt", "voc_call_cnt", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 被动通话记录占比
    def passive_voc_ratio(self):
        column_name = "passive_voc_ratio"
        if column_name not in self.data.columns:
            print("---正在加工被动通话记录占比")
            self.voc_call_cnt()
            self.passive_voc_call_cnt()
            self.division("passive_voc_call_cnt", "voc_call_cnt", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 呼转通话记录占比
    def turn_voc_ratio(self):
        column_name = "turn_voc_ratio"
        if column_name not in self.data.columns:
            print("---正在加工呼转通话记录占比")
            self.voc_call_cnt()
            self.turn_voc_call_cnt()
            self.division("turn_voc_call_cnt", "voc_call_cnt", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 通话记录条数
    def voc_call_cnt(self, is_call=True):
        column_name = "voc_call_cnt" if is_call else "sms_cnt"
        text_type = "通话" if is_call else "短信"
        self.voc_type_call_cnt(column_name, is_call=is_call, text="---正在加工用户总"+text_type+"记录条数")
        return self.data[["phone_no_m", column_name]]

    # 主动通话记录条数
    def initiative_voc_call_cnt(self, is_call=True):
        column_name = "initiative_voc_call_cnt" if is_call else "initiative_sms_cnt"
        text_type = "通话" if is_call else "短信"
        self.voc_type_call_cnt(column_name, is_call=is_call, text="---正在加工用户总主动"+text_type+"记录条数", call_type_id=1)
        return self.data[["phone_no_m", column_name]]

    # 被动通话记录条数
    def passive_voc_call_cnt(self, is_call=True):
        column_name = "passive_voc_call_cnt" if is_call else "passive_sms_cnt"
        text_type = "通话" if is_call else "短信"
        self.voc_type_call_cnt(column_name, is_call=is_call, text="---正在加工用户总被动"+text_type+"记录条数", call_type_id=2)
        return self.data[["phone_no_m", column_name]]

    # 呼转通话记录条数
    def turn_voc_call_cnt(self):
        column_name = "turn_voc_call_cnt"
        self.voc_type_call_cnt(column_name, is_call=True, text="---正在加工用户总呼转通话记录条数", call_type_id=3)
        return self.data[["phone_no_m", column_name]]

    # 通话记录条数
    def voc_type_call_cnt(self, column_name, is_call, text, call_type_id=0):
        if column_name not in self.data.columns:
            print(text)
            tmp_data = self.voc if is_call else self.sms
            tmp_data = tmp_data[tmp_data["calltype_id"] == call_type_id] if call_type_id > 0 else self.voc
            tmp_data = func_count(tmp_data[["phone_no_m", "opposite_no_m"]], "phone_no_m", "opposite_no_m")
            self.add_to_data(tmp_data, [column_name])

    # 一天中通话记录条数
    def voc_inner_day_call_cnt(self):
        column_name = "voc_inner_day_call_cnt"
        self.voc_type_inner_day_call_cnt(column_name, "---正在加工一天中通话记录条数")
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 一天中主动通话记录条数
    def initiative_voc_inner_day_call_cnt(self):
        column_name = "initiative_voc_inner_day_call_cnt"
        self.voc_type_inner_day_call_cnt(column_name, "---正在加工一天中主动通话记录条数", calltype_id=1)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 一天中被动通话记录条数
    def passive_voc_inner_day_call_cnt(self):
        column_name = "passive_voc_inner_day_call_cnt"
        self.voc_type_inner_day_call_cnt(column_name, "---正在加工一天中被动通话记录条数", calltype_id=2)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 一天中呼转通话记录条数
    def turn_voc_inner_day_call_cnt(self):
        column_name = "turn_voc_inner_day_call_cnt"
        self.voc_type_inner_day_call_cnt(column_name, "---正在加工一天中呼转通话记录条数", calltype_id=3)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 一天中通话记录条数
    def voc_type_inner_day_call_cnt(self, column_name, text, calltype_id=0):
        if column_name + "_min" not in self.data.columns:
            print(text)
            tmp_data = self.voc[self.voc["calltype_id"] == calltype_id].copy() if calltype_id > 0 else self.voc.copy()
            tmp_data["start_date"] = tmp_data[["start_datetime"]].apply(lambda x: x[0][0:10], axis=1)
            tmp_data = func_count(tmp_data[["phone_no_m", "start_date", "opposite_no_m"]].copy(),
                                  ["phone_no_m", "start_date"], "opposite_no_m").reset_index()
            tmp_data.columns = ["phone_no_m", "start_date", column_name]
            self.agg_function(tmp_data, "phone_no_m", column_name)

    # 一天中有过通话记录的不同用户数
    def voc_inner_day_user_cnt(self):
        column_name = "voc_inner_day_user_cnt"
        self.voc_type_inner_day_user_cnt(column_name, "---正在加工一天中有过通话记录的不同用户数")
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median", column_name + "_mean"]]

    # 一天中有过主动通话记录的不同用户数
    def initiative_voc_inner_day_user_cnt(self):
        column_name = "initiative_voc_inner_day_user_cnt"
        self.voc_type_inner_day_user_cnt(column_name, "---正在加工一天中有过主动通话记录的不同用户数", calltype_id=1)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 一天中有过被动通话记录的不同用户数
    def passive_voc_inner_day_user_cnt(self):
        column_name = "passive_voc_inner_day_user_cnt"
        self.voc_type_inner_day_user_cnt(column_name, "---正在加工一天中有过被动通话记录的不同用户数", calltype_id=2)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 一天中有过呼转通话记录的不同用户数
    def turn_voc_inner_day_user_cnt(self):
        column_name = "turn_voc_inner_day_user_cnt"
        self.voc_type_inner_day_user_cnt(column_name, "---正在加工一天中有过呼转通话记录的不同用户数", calltype_id=3)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 一天中有过通话记录的不同用户数
    def voc_type_inner_day_user_cnt(self, column_name, text, calltype_id=0):
        if column_name + "_min" not in self.data.columns:
            print(text)
            tmp_data = self.voc[self.voc["calltype_id"]==calltype_id].copy() if calltype_id>0 else self.voc.copy()
            tmp_data["start_date"] = tmp_data[["start_datetime"]].apply(lambda x: x[0][0:10], axis=1)
            tmp_data = func_count_distinct(tmp_data[["phone_no_m", "start_date", "opposite_no_m"]].copy(),
                                           ["phone_no_m", "start_date"], "opposite_no_m").reset_index()
            tmp_data.columns = ["phone_no_m", "start_date", column_name]
            self.agg_function(tmp_data, "phone_no_m", column_name)

    # 用户通话记录中对方号码个数
    def voc_user_cnt(self):
        column_name="voc_user_cnt"
        self.voc_type_user_cnt(column_name, "---正在加工用户通话记录中对方号码个数")
        return self.data[["phone_no_m", column_name]]

    # 主呼通话记录中对方号码个数
    def initiative_voc_user_cnt(self):
        column_name = "initiative_voc_user_cnt"
        self.voc_type_user_cnt(column_name, "---正在加工主呼通话记录中对方号码个数", 1)
        return self.data[["phone_no_m", column_name]]

    # 被呼通话记录中对方号码个数
    def passive_voc_user_cnt(self):
        column_name = "passive_voc_user_cnt"
        self.voc_type_user_cnt(column_name, "---正在加工被呼通话记录中对方号码个数", 2)
        return self.data[["phone_no_m", column_name]]

    # 呼转通话记录中对方号码个数
    def turn_voc_user_cnt(self):
        column_name = "turn_voc_user_cnt"
        self.voc_type_user_cnt(column_name, "---正在加工呼转通话记录中对方号码个数", 3)
        return self.data[["phone_no_m", column_name]]

    # 用户短信记录中对方号码个数
    def sms_user_cnt(self):
        column_name = "sms_user_cnt"
        self.voc_type_user_cnt(column_name, "---正在加工用户短信记录中对方号码个数", is_call=False)
        return self.data[["phone_no_m", column_name]]

    # 用户主动发送短信记录中对方号码个数
    def initiative_sms_user_cnt(self):
        column_name = "initiative_sms_user_cnt"
        self.voc_type_user_cnt(column_name, "---正在加工用户主动发送短信记录中对方号码个数",
                               is_call=False, call_type_id=1)
        return self.data[["phone_no_m", column_name]]

    # 用户被动接收短信记录中对方号码个数
    def passive_sms_user_cnt(self):
        column_name = "passive_sms_user_cnt"
        self.voc_type_user_cnt(column_name, "---正在加工用户被动接收短信记录中对方号码个数",
                               is_call=False, call_type_id=2)
        return self.data[["phone_no_m", column_name]]

    # 加工通话记录中用户的数量
    def voc_type_user_cnt(self, column_name, text, call_type_id=0, is_call=True):
        if column_name not in self.data.columns:
            print(text)
            temp_data = (self.get_single_voc_data("opposite_no_m", call_type_id=call_type_id) if is_call
                         else self.get_single_sms_data("opposite_no_m", call_type_id=call_type_id))
            temp_data = func_count_distinct(temp_data, "phone_no_m", "opposite_no_m")
            self.add_to_data(temp_data, [column_name])

    # 与同一个人的通话次数
    def voc_user_call_cnt(self):
        column_name = "voc_user_call_cnt"
        self.voc_type_user_call_cnt(column_name, "---正在与同一个人的通话次数")
        return self.data[["phone_no_m", column_name+"_max", column_name+"_min", column_name+"_median", column_name+"_mean"]]

    # 与同一个人的主动通话次数
    def initiative_voc_user_call_cnt(self):
        column_name = "initiative_voc_user_call_cnt"
        self.voc_type_user_call_cnt(column_name, "---正在与同一个人的主动通话次数", call_type_id=1)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 与同一个人的被动通话次数
    def passive_voc_user_call_cnt(self):
        column_name = "passive_voc_user_call_cnt"
        self.voc_type_user_call_cnt(column_name, "---正在与同一个人的被动通话次数", call_type_id=2)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 与同一个人的呼转通话次数
    def turn_voc_user_call_cnt(self):
        column_name = "turn_voc_user_call_cnt"
        self.voc_type_user_call_cnt(column_name, "---正在与同一个人的呼转通话次数", call_type_id=3)
        return self.data[["phone_no_m", column_name + "_max", column_name + "_min", column_name + "_median",
                          column_name + "_mean"]]

    # 与同一个人的通话次数加工逻辑
    def voc_type_user_call_cnt(self, column_name, text, call_type_id=0):
        if column_name + "_max" not in self.data.columns:
            print(text)
            temp_data = self.voc[self.voc["calltype_id"]==call_type_id] if call_type_id>0 else self.voc
            temp_data = func_count(temp_data[["phone_no_m", "opposite_no_m", "calltype_id"]].copy(),
                                   ["phone_no_m", "opposite_no_m"], "calltype_id").reset_index()
            temp_data.columns = ['phone_no_m', 'opposite_no_m', column_name]
            self.agg_function(temp_data, "phone_no_m", column_name)

    # 聚合函数
    def agg_function(self, data, key, column_name):
        temp_data = data.groupby(key).agg({column_name: [np.max, np.min, np.median, np.mean]})
        self.add_to_data(temp_data, [column_name + "_max", column_name + "_min", column_name + "_median", column_name + "_mean"])

    # 计算各用户的电话记录之间的通话间隔
    def voc_interval(self):
        columns = self.voc_type_interval_cnt("---正在计算各用户的电话记录之间的通话间隔")
        return self.data[columns]

    # 计算各用户的主动拨打电话记录之间的通话间隔
    def initiative_voc_interval(self):
        columns = self.voc_type_interval_cnt("---正在计算各用户的主动拨打电话记录之间的通话间隔", call_type_id=1)
        return self.data[columns]

    # 计算各用户的被动接听电话记录之间的通话间隔
    def passive_voc_interval(self):
        columns = self.voc_type_interval_cnt("---正在计算各用户的被动接听电话记录之间的通话间隔", call_type_id=2)
        return self.data[columns]

    # 计算各用户的呼转电话记录之间的通话间隔
    def turn_voc_interval(self):
        columns = self.voc_type_interval_cnt("---正在计算各用户的呼转电话记录之间的通话间隔", call_type_id=3)
        return self.data[columns]

    def voc_type_interval_cnt(self, text, call_type_id=0):
        columns = ["voc_interval_min", "voc_interval_max", "voc_interval_mean",
                   "voc_interval_median", "voc_interval_std"]
        if call_type_id == 1:
            columns = ["initiative_"+str(x) for x in columns]
        elif call_type_id == 2:
            columns = ["passive_" + str(x) for x in columns]
        elif call_type_id == 3:
            columns = ["turn_" + str(x) for x in columns]
        else:
            columns = [str(x) for x in columns]
        if columns[0] not in self.data.columns:
            print(text)
            temp_data = self.voc[self.voc["calltype_id"]==call_type_id] if call_type_id>0 else self.voc
            final_result = calculate_interval(
                temp_data[["phone_no_m", "start_datetime", "call_dur"]].copy(),
                self.user[["phone_no_m", "label"]],
                columns).set_index("phone_no_m")[columns].copy()
            self.add_to_data(final_result[columns].copy(), columns)
        return columns

    # 通话记录中出现的不同imei的个数
    def voc_imei_cnt(self):
        self.voc_type_imei_cnt()
        return self.data[["phone_no_m", self.column_name.columns_voc_imei_cnt[0]]]

    # 主动拨打电话记录中出现的不同imei的个数
    def initiative_voc_imei_cnt(self):
        self.voc_type_imei_cnt(call_type_id=1)
        return self.data[["phone_no_m", self.column_name.columns_voc_imei_cnt[1]]]

    # 被动接听电话记录中出现的不同imei的个数
    def passive_voc_imei_cnt(self):
        self.voc_type_imei_cnt(call_type_id=2)
        return self.data[["phone_no_m", self.column_name.columns_voc_imei_cnt[2]]]

    # 呼转电话记录中出现的不同imei的个数
    def turn_voc_imei_cnt(self):
        self.voc_type_imei_cnt(call_type_id=3)
        return self.data[["phone_no_m", self.column_name.columns_voc_imei_cnt[3]]]

    # IMEI数量加工
    def voc_type_imei_cnt(self, call_type_id=0):
        column_name = self.column_name.columns_voc_imei_cnt[call_type_id]
        if column_name not in self.data.columns:
            print("---正在加工"+self.column_name.voc_type[call_type_id]+"中出现的imei个数")
            temp_data = self.voc[self.voc["calltype_id"]==call_type_id] if call_type_id>0 else self.voc
            temp_data = func_count_distinct(temp_data.dropna(subset=["imei_m"])[["phone_no_m", "imei_m"]].copy(),
                                            "phone_no_m", "imei_m")
            temp_data.columns = [column_name]
            self.add_to_data(temp_data, [column_name])

    # 通话总时长
    def voc_dur(self):
        self.voc_type_call_dur()
        return self.data[["phone_no_m", self.column_name.columns_voc_call_dur[0]]]

    # 主动拨打通话总时长
    def initiative_voc_dur(self):
        self.voc_type_call_dur(call_type_id=1)
        return self.data[["phone_no_m", self.column_name.columns_voc_call_dur[1]]]

    # 被动接听通话总时长
    def passive_voc_dur(self):
        self.voc_type_call_dur(call_type_id=2)
        return self.data[["phone_no_m", self.column_name.columns_voc_call_dur[2]]]

    # 呼转通话总时长
    def turn_voc_dur(self):
        self.voc_type_call_dur(call_type_id=3)
        return self.data[["phone_no_m", self.column_name.columns_voc_call_dur[3]]]

    # 通话总时长
    def voc_type_call_dur(self, call_type_id=0):
        column_name = self.column_name.columns_voc_call_dur[call_type_id]
        if column_name not in self.data.columns:
            print("---正在加工" + self.column_name.voc_type[call_type_id] + "总时长")
            temp_data = func_sum(self.get_single_voc_data("call_dur", call_type_id=call_type_id),
                                 "phone_no_m", "call_dur")
            temp_data.columns = [column_name]
            self.add_to_data(temp_data, [column_name])

    # 主动拨打电话总时长占通话记录总时长占比
    def initiative_voc_dur_ratio(self):
        column_name = "initiative_voc_dur_ratio"
        if column_name not in self.data.columns:
            print("---正在加工主动拨打电话总时长占通话记录总时长占比")
            self.voc_dur()
            self.initiative_voc_dur()
            self.division("initiative_voc_dur", "voc_dur", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]].copy()

    # 被动接听电话总时长占通话记录总时长占比
    def passive_voc_dur_ratio(self):
        column_name = "passive_voc_dur_ratio"
        if column_name not in self.data.columns:
            print("---正在加工被动接听电话总时长占通话记录总时长占比")
            self.voc_dur()
            self.passive_voc_dur()
            self.division("passive_voc_dur", "voc_dur", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]].copy()

    # 呼转电话总时长占通话记录总时长占比
    def turn_voc_dur_ratio(self):
        column_name = "turn_voc_dur_ratio"
        if column_name not in self.data.columns:
            print("---正在加工呼转电话总时长占通话记录总时长占比")
            self.voc_dur()
            self.turn_voc_dur()
            self.division("turn_voc_dur", "voc_dur", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]].copy()

    # 拨打电话的活跃天数
    def voc_active_days(self):
        self.voc_type_active_days()
        return self.data[["phone_no_m", self.column_name.columns_voc_active_days[0]]]

    # 主动拨打电话的活跃天数
    def initiative_voc_active_days(self):
        self.voc_type_active_days(call_type_id=1)
        return self.data[["phone_no_m", self.column_name.columns_voc_active_days[1]]]

    # 被动拨打电话的活跃天数
    def passive_voc_active_days(self):
        self.voc_type_active_days(call_type_id=2)
        return self.data[["phone_no_m", self.column_name.columns_voc_active_days[2]]]

    # 呼转电话的活跃天数
    def turn_voc_active_days(self):
        self.voc_type_active_days(call_type_id=3)
        return self.data[["phone_no_m", self.column_name.columns_voc_active_days[3]]]

    # 短信的活跃天数
    def sms_active_days(self):
        self.voc_type_active_days(is_call=False)
        return self.data[["phone_no_m", self.column_name.columns_sms_active_days[0]]]

    # 主动发送短信的活跃天数
    def initiative_sms_active_days(self):
        self.voc_type_active_days(is_call=False, call_type_id=1)
        return self.data[["phone_no_m", self.column_name.columns_sms_active_days[1]]]

    # 被动接收短信的活跃天数
    def passive_sms_active_days(self):
        self.voc_type_active_days(is_call=False, call_type_id=2)
        return self.data[["phone_no_m", self.column_name.columns_sms_active_days[2]]]

    # 活跃天数
    def voc_type_active_days(self, call_type_id=0, is_call=True):
        column_name = (self.column_name.columns_voc_active_days[call_type_id] if is_call
                       else self.column_name.columns_sms_active_days[call_type_id])
        if column_name not in self.data.columns:
            text = self.column_name.voc_type[call_type_id] if is_call else self.column_name.sms_type[call_type_id]
            target_column = "start_datetime" if is_call else "request_datetime"
            print("---正在加工"+text+"的活跃天数")
            temp_data = (self.get_single_voc_data(target_column, call_type_id=call_type_id) if is_call
                         else self.get_single_sms_data(target_column, call_type_id=call_type_id))
            temp_data["date"] = temp_data.apply(lambda x: convert_datetime_to_date(x, target_column), axis=1)
            temp_data.dropna(subset=["date"], inplace=True)
            temp_data = func_count_distinct(temp_data, "phone_no_m", "date")
            self.add_to_data(temp_data, [column_name])

    # 通话记录中与同一用户通讯的持续天数
    def voc_user_contact_days(self):
        column_name = self.column_name.prefix_voc_type[0]+"voc_user_contact_days"
        self.voc_type_user_contact_days()
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median", column_name + "_mean"]]

    # 主动拨打电话记录中与同一用户通讯的持续天数
    def initiative_voc_user_contact_days(self):
        column_name = self.column_name.prefix_voc_type[1] + "voc_user_contact_days"
        self.voc_type_user_contact_days(call_type_id=1)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 被动接听电话记录中与同一用户通讯的持续天数
    def passive_voc_user_contact_days(self):
        column_name = self.column_name.prefix_voc_type[2] + "voc_user_contact_days"
        self.voc_type_user_contact_days(call_type_id=2)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 呼转电话记录中与同一用户通讯的持续天数
    def turn_voc_user_contact_days(self):
        column_name = self.column_name.prefix_voc_type[3] + "voc_user_contact_days"
        self.voc_type_user_contact_days(call_type_id=3)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 通话记录和短信记录中与同一用户通讯的持续天数
    def voc_type_user_contact_days(self, call_type_id=0, is_call=True):
        column_name = "voc" if is_call else "sms"
        column_name = self.column_name.prefix_voc_type[call_type_id]+column_name+"_user_contact_days"
        if column_name+"_min" not in self.data.columns:
            text = "通话记录" if is_call else "短信记录"
            print("---正在加工" + text + "中与同一用户的联系天数")

            target_name = "start_datetime" if is_call else "request_datetime"
            temp_data = self.voc.copy() if is_call else self.sms.copy()
            temp_data = temp_data[temp_data["calltype_id"] == call_type_id].copy() if call_type_id>0 else temp_data.copy()
            temp_data["date"] = temp_data.apply(lambda x: convert_datetime_to_date(x, target_name), axis=1)

            # 丢弃值为空的数据
            temp_data.dropna(subset=["opposite_no_m"], inplace=True)
            temp_data.dropna(subset=["date"], inplace=True)

            # 计算用户与其每一位通讯对象进行通讯的最早日期和最晚日期
            temp_data = temp_data.groupby(["phone_no_m", "opposite_no_m"]).agg({"date": [np.min, np.max]}).reset_index()
            temp_data.columns = ["phone_no_m", "opposite_no_m", "start_date", "end_date"]

            # 计算用户与其每一位通讯对象进行通讯的最早日期和最晚日期的天数差
            temp_data[column_name] = temp_data.apply(lambda x: (dt.datetime.strptime(x["end_date"], "%Y-%m-%d")-
                                       dt.datetime.strptime(x["start_date"], "%Y-%m-%d")).days+1,axis=1)

            self.agg_function(temp_data, "phone_no_m", column_name)
        return self.data[["phone_no_m", column_name+"_min", column_name+"_max", column_name+"_median", column_name+"_mean"]]

    # 用户主动拨打电话的活跃天数和被动接听电话的活跃天数差值
    def call_activate_days_diff(self):
        column_name = "call_activate_days_diff"
        if column_name not in self.data.columns:
            print("---正在加工用户主动拨打电话的活跃天数和被动接听电话的活跃天数差值")
            self.initiative_voc_active_days()
            self.passive_voc_active_days()
            self.data[column_name] = self.data.apply(lambda x: x["initiative_voc_active_days"]-x["passive_voc_active_days"], axis=1)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 用户主动发送短信的活跃天数和被动接听电话的活跃天数差值
    def sms_activate_days_diff(self):
        column_name = "sms_activate_days_diff"
        if column_name not in self.data.columns:
            print("---正在加工用户主动发送短信的活跃天数和被动接听电话的活跃天数差值")
            self.initiative_sms_active_days()
            self.passive_sms_active_days()
            self.data[column_name] = self.data.apply(lambda x: x["initiative_sms_active_days"] - x["passive_sms_active_days"], axis=1)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 用户一小时内的通话数量
    def voc_inner_hour_cnt(self):
        column_name = self.column_name.prefix_voc_type[0]+"voc_inner_hour_cnt"
        self.voc_type_inner_hour_cnt()
        return self.data[["phone_no_m", column_name+"_min", column_name+"_max", column_name+"_median", column_name+"_mean"]]

    # 用户主动拨打电话记录中每小时的通讯数量
    def initiative_voc_inner_hour_cnt(self):
        column_name = self.column_name.prefix_voc_type[1] + "voc_inner_hour_cnt"
        self.voc_type_inner_hour_cnt(call_type_id=1)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median", column_name + "_mean"]]

    # 用户主动拨打电话记录中每小时的通讯数量
    def passive_voc_inner_hour_cnt(self):
        column_name = self.column_name.prefix_voc_type[2] + "voc_inner_hour_cnt"
        self.voc_type_inner_hour_cnt(call_type_id=2)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median", column_name + "_mean"]]

    # 用户呼转电话记录中每小时的通讯数量
    def turn_voc_inner_hour_cnt(self):
        column_name = self.column_name.prefix_voc_type[3] + "voc_inner_hour_cnt"
        self.voc_type_inner_hour_cnt(call_type_id=3)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median", column_name + "_mean"]]

    # 用户短信记录中每小时的短信数量
    def sms_inner_hour_cnt(self):
        column_name = self.column_name.prefix_voc_type[0] + "sms_inner_hour_cnt"
        self.voc_type_inner_hour_cnt(is_call=False)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 用户主动发送短信记录中每小时的短信数量
    def initiative_sms_inner_hour_cnt(self):
        column_name = self.column_name.prefix_voc_type[1] + "sms_inner_hour_cnt"
        self.voc_type_inner_hour_cnt(is_call=False, call_type_id=1)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 用户被动接受短信记录中每小时的短信数量
    def passive_sms_inner_hour_cnt(self):
        column_name = self.column_name.prefix_voc_type[2] + "sms_inner_hour_cnt"
        self.voc_type_inner_hour_cnt(is_call=False, call_type_id=2)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 用户一小时内的通讯数量
    def voc_type_inner_hour_cnt(self, call_type_id=0, is_call=True):
        column_name = "voc" if is_call else "sms"
        column_name = self.column_name.prefix_voc_type[call_type_id]+column_name+"_inner_hour_cnt"
        if column_name+"_min" not in self.data.columns:
            text = self.column_name.voc_type[call_type_id] if is_call else self.column_name.sms_type[call_type_id]
            print("---正在计算用户"+text+"中每小时的通讯数量")
            temp_data = self.voc.copy() if is_call else self.sms.copy()
            temp_data = temp_data[temp_data["calltype_id"]==call_type_id].copy() if call_type_id>0 else temp_data.copy()
            target_name = "start_datetime" if is_call else "request_datetime"
            temp_data["hour"] = temp_data.apply(lambda x: x[target_name][0:13], axis=1)

            temp_data = func_count(temp_data, ["phone_no_m", "hour"], "calltype_id").reset_index()
            temp_data.columns = ["phone_no_m", "hour", column_name]

            self.agg_function(temp_data, "phone_no_m", column_name)

    # 用户每天通话时长
    def voc_inner_day_dur(self):
        column_name = self.column_name.prefix_voc_type[0] + "voc_inner_day_dur"
        self.voc_type_inner_day_dur()
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 用户每天主动拨打电话时长
    def initiative_voc_inner_day_dur(self):
        column_name = self.column_name.prefix_voc_type[1] + "voc_inner_day_dur"
        self.voc_type_inner_day_dur(call_type_id=1)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 用户每天主动拨打电话时长
    def passive_voc_inner_day_dur(self):
        column_name = self.column_name.prefix_voc_type[2] + "voc_inner_day_dur"
        self.voc_type_inner_day_dur(call_type_id=2)
        return self.data[["phone_no_m", column_name + "_min", column_name + "_max", column_name + "_median",
                          column_name + "_mean"]]

    # 用户每天通话时长
    def voc_type_inner_day_dur(self, call_type_id=0, is_call=True):
        column_name = "voc" if is_call else "sms"
        column_name = self.column_name.prefix_voc_type[call_type_id] + column_name + "_inner_day_dur"
        if column_name+"_min" not in self.data.columns:
            text = self.column_name.voc_type[call_type_id] if is_call else self.column_name.sms_type[call_type_id]
            print("---正在计算用户" + text + "中每天的通讯时长")

            temp_data = self.voc.copy() if is_call else self.sms.copy()
            temp_data = temp_data[temp_data["calltype_id"] == call_type_id].copy() if call_type_id > 0 else temp_data.copy()
            target_name = "start_datetime" if is_call else "request_datetime"
            temp_data["date"] = temp_data.apply(lambda x: convert_datetime_to_date(x, target_name), axis=1)

            # 计算用户每日的通话时长
            temp_data = func_sum(temp_data, ["phone_no_m", "date"], "call_dur").reset_index()
            temp_data.columns = ["phone_no_m", "date", column_name]

            self.agg_function(temp_data, "phone_no_m", column_name)

    # 通话记录中与用户同时有拨打电话和接听电话的好友数
    def interactive_voc_user_cnt(self):
        self.interactive_user_cnt()
        return self.data[["phone_no_m", "interactive_voc_user_cnt"]]

    # 短信记录中与用户同时有发送短信和接收短信的好友数
    def interactive_sms_user_cnt(self):
        self.interactive_user_cnt(is_call=False)
        return self.data[["phone_no_m", "interactive_sms_user_cnt"]]

    # 与用户同时有主动联系和被动联系的好友数
    def interactive_user_cnt(self, is_call=True):
        column_name = "voc" if is_call else "sms"
        column_name = "interactive_"+column_name+"_user_cnt"
        if column_name not in self.data.columns:
            text = "通话记录" if is_call else "短信记录"
            print("---正在加工"+text+"中有交互的用户数")
            temp_data = (self.voc[["phone_no_m", "opposite_no_m", "calltype_id"]].copy() if is_call
                         else self.sms[["phone_no_m", "opposite_no_m", "calltype_id"]].copy())
            temp_data.dropna(subset=["opposite_no_m"], inplace=True)
            temp_data.dropna(subset=["calltype_id"], inplace=True)

            # 标记与用户有主动通话或被动通话的记录
            temp_data["initiative_type"] = temp_data.apply(lambda x: 1 if x["calltype_id"]==1 else 0, axis=1)
            temp_data["passive_type"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)
            temp_data = temp_data.groupby(["phone_no_m", "opposite_no_m"]).agg({
                "initiative_type": [pd.Series.max],
                "passive_type": [pd.Series.max]
            }).reset_index()
            temp_data.columns = ["phone_no_m", "opposite_no_m", "initiative_type", "passive_type"]

            # 标记与用户同时有主动通话和被动通话的记录
            temp_data[column_name] = temp_data.apply(lambda x: 1 if ((x["initiative_type"]==1) and (x["passive_type"]==1)) else 0, axis=1)

            temp_data = func_sum(temp_data, "phone_no_m", column_name)
            self.add_to_data(temp_data, [column_name])

    # 通话记录中与用户同时有拨打电话和接听电话的好友比例
    def interactive_voc_user_ratio(self):
        column_name = "interactive_voc_user_ratio"
        if column_name not in self.data.columns:
            print("---正在加工通话记录中与用户同时有拨打电话和接听电话的好友比例")
            self.voc_user_cnt()
            self.interactive_voc_user_cnt()
            self.division("interactive_voc_user_cnt", "voc_user_cnt", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 短信记录中与用户同时有发送短信和接收短信的好友比例
    def interactive_sms_user_ratio(self):
        column_name = "interactive_sms_user_ratio"
        if column_name not in self.data.columns:
            print("---正在加工短信记录中与用户同时有发送短信和接收短信的好友比例")
            self.sms_user_cnt()
            self.interactive_sms_user_cnt()
            self.division("interactive_sms_user_cnt", "sms_user_cnt", column_name)
            self.print_correlation(column_name)
        return self.data[["phone_no_m", column_name]]

    # 夜间通话占比较高
    def night_voc_ratio_too_high(self):
        column_name = "night_voc_ratio_too_high"
        if column_name not in self.data.columns:
            print("--- 夜间通话占比较高")
            temp_data = self.voc.copy()
            temp_data["hour"] = temp_data.apply(
                lambda x: 1 if ((int(x["start_datetime"][11:13]) < 6) or (int(x["start_datetime"][11:13]) == 23)) else 0,
                axis=1)
            agg_data = temp_data.groupby("phone_no_m").agg(voc_cnt=("hour", pd.Series.count),
                                                           night_voc_cnt=("hour", pd.Series.sum))
            agg_data["night_voc_ratio"] = agg_data.apply(lambda x: round(x["night_voc_cnt"] / x["voc_cnt"], 4), axis=1)
            agg_data["night_voc_ratio_too_high"] = agg_data.apply(lambda x: 1 if x["night_voc_ratio"]>=0.6 else 0, axis=1)
            self.data = self.data.join(agg_data[["night_voc_ratio_too_high"]], on="phone_no_m").fillna(0)
        return self.data[["phone_no_m", column_name]]

    # 是否安装微信
    def has_we_chat(self):
        column_name = "has_we_chat"
        if column_name not in self.data.columns:
            print("--- 是否安装微信")
            temp_data = self.app[self.app["busi_name"] == "微信"]["phone_no_m"].values.tolist()
            self.data["has_we_chat"] = self.data.apply(lambda x: 1 if x["phone_no_m"] in temp_data else 0, axis=1)
        return self.data[["phone_no_m", column_name]]

    # imei数量相关特征
    def imei_cnt_about(self):
        column_name = "has_no_imei"
        if column_name not in self.data.columns:
            print("--- imei数量相关特征")
            self.voc_imei_cnt()
            self.data["has_no_imei"] = self.data.apply(lambda x: 1 if x["voc_imei_cnt"] == 0 else 0, axis=1)
            self.data["too_many_imei"] = self.data.apply(lambda x: 1 if x["voc_imei_cnt"] >= 2 else 0, axis=1)
            self.data["except_imei"] = self.data.apply(lambda x: 1 if x["voc_imei_cnt"] != 1 else 0, axis=1)
        return self.data[["phone_no_m", "has_no_imei", "too_many_imei", "except_imei"]]

    # 高频拨打电话
    def frequency_initiative_voc(self):
        column_name = "frequency_initiative_voc"
        if column_name not in self.data.columns:
            # 主动通话的通话记录中，持续联系天数在一天的用户数
            print("--- 主动通话的通话记录中，持续联系天数在一天的用户数")
            temp_data = self.voc[self.voc["calltype_id"] == 1][["phone_no_m", "opposite_no_m", "start_datetime"]].copy()
            temp_data["date"] = temp_data.apply(lambda x: x["start_datetime"][0:10], axis=1)
            agg_data = (temp_data.groupby(["phone_no_m", "opposite_no_m"])
                        .agg(first_date=("date", pd.Series.min), last_date=("date", pd.Series.max))
                        .reset_index())
            agg_data["one_day_contact"] = agg_data.apply(lambda x: 1 if x["first_date"] == x["last_date"] else 0, axis=1)
            result_data = self.user[["phone_no_m", "label"]].join(
                (agg_data.groupby("phone_no_m")
                 .agg(user_cnt=("opposite_no_m", pd.Series.nunique),
                      one_day_user_cnt=("one_day_contact", pd.Series.sum))), on=["phone_no_m"]).fillna(0)
            result_data["one_day_ratio"] = result_data.apply(lambda x: round(x["one_day_user_cnt"] / x["user_cnt"], 2)
                if x["user_cnt"] > 0 else 0, axis=1)
            result_data["frequency_initiative_voc"] = result_data.apply(lambda x: 1 if x["one_day_ratio"] >= 0.87 else 0, axis=1)
            self.data = self.data.join(result_data[["phone_no_m", "one_day_user_cnt", "one_day_ratio", "frequency_initiative_voc"]].set_index("phone_no_m"),
                                       on="phone_no_m")
        return self.data[["phone_no_m", "one_day_user_cnt", "one_day_ratio", "frequency_initiative_voc"]]

    # 用户是否安装APP
    def has_app(self):
        column_name = "has_app"
        if column_name not in self.data.columns:
            print("--- 用户是否安装APP")
            self.app_cnt()
            self.data[column_name] = self.data.apply(lambda x: 1 if x["app_cnt"] > 0 else 0, axis=1)
        return self.data[["phone_no_m", column_name]]

    # 最后一次通话时间在24号之前
    def last_call_is_before_24(self):
        column_name = "last_call_is_before_24"
        if column_name not in self.data.columns:
            print("--- 正在判断最后一次通话时间在24号之前")
            temp_data = self.voc[["phone_no_m", "start_datetime"]].copy()
            temp_data["voc_last_day"] = temp_data.apply(lambda x: int(x["start_datetime"][8:10]),
                                                        axis=1)
            agg_data = self.user[["phone_no_m", "label"]].join(temp_data.groupby("phone_no_m")
                                                           .agg(last_day=("voc_last_day", pd.Series.max)),
                                                           on=["phone_no_m"]).fillna(0)
            target_phones = list(set(agg_data[agg_data["last_day"] <= 24]["phone_no_m"].values))
            self.data[column_name] = self.data.apply(lambda x: 1 if x["phone_no_m"] in target_phones else 0, axis=1)
        return self.data[["phone_no_m", column_name]]

    # 身份证下手机号过多
    def has_too_many_id_card(self):
        column_name = "has_too_many_id_card"
        if column_name not in self.data.columns:
            print("--- 正在判断用户身份证下手机号过多")
            self.data[column_name] = self.data.apply(lambda x: 1 if x["idcard_cnt"] > 2 else 0, axis=1)
        return self.data[["phone_no_m", column_name]]

    # 主呼中联系人数过多
    def initiative_voc_has_too_many_phone(self):
        column_name = "initiative_voc_has_too_many_phone"
        if column_name not in self.data.columns:
            print("--- 主呼中联系人数过多")
            self.initiative_voc_user_cnt()
            self.data[column_name] = self.data.apply(lambda x: 1 if x["initiative_voc_user_cnt"] > 57 else 0, axis=1)
        return self.data[["phone_no_m", column_name]]

    # 被呼平均通话时长过短
    def passive_voc_avg_dur_too_low(self):
        column_name = "passive_voc_avg_dur_too_low"
        if column_name not in self.data.columns:
            print("--- 被呼平均通话时长过短")
            temp_data = self.voc[self.voc["calltype_id"] == 2][["phone_no_m", "call_dur"]].copy()
            agg_data = temp_data.groupby("phone_no_m").agg(passive_voc_dur_mean=("call_dur", pd.Series.mean)).reset_index()
            no_target_phones = list(set(agg_data[agg_data["passive_voc_dur_mean"] > 18]["phone_no_m"].values))
            self.data[column_name] = self.data.apply(lambda x: 0 if x["phone_no_m"] in no_target_phones else 1, axis=1)
        return self.data[["phone_no_m", column_name]]

    # 通话记录中是否包含区域
    def has_county(self):
        column_name = "has_county"
        if column_name not in self.data.columns:
            print("--- 通话记录中是否包含区域")
            temp_data = self.voc[["phone_no_m", "county_name"]].drop_duplicates().copy()
            agg_data = temp_data.groupby("phone_no_m").agg(county_cnt=("county_name", pd.Series.nunique)).reset_index()
            no_target_phones = list(set(agg_data[agg_data["county_cnt"]>0]["phone_no_m"].values))
            self.data[column_name] = self.data.apply(lambda x: 0 if x["phone_no_m"] in no_target_phones else 1, axis=1)
        return self.data[["phone_no_m", column_name]]

    # 用来做规则的APP列表
    def is_hit_rule_app(self):
        high_risk_app = ["海康威视", "杭州狂想网络科技有限公司官网", "Vypr VPN", "捞月狗", "XianJinBaShi", "安游在线", "联动优势"]
        column_name = "is_hit_rule_app"
        if column_name not in self.data.columns:
            print("--- 正在判断用户安装的app中是否有高危APP")
            temp_data = list(set(self.app[self.app.apply(lambda x: True if x["busi_name"] in high_risk_app else False, axis=1)]["phone_no_m"].values))
            self.data[column_name] = self.data.apply(lambda x: 1 if x["phone_no_m"] in temp_data else 0, axis=1)
        return self.data[["phone_no_m", column_name]]

    # 通话记录中是否有高危用户
    def is_hit_rule_opposite(self):
        column_name = "is_hit_rule_opposite"
        if column_name not in self.data.columns:
            print("--- 通话记录中是否有高危用户")
            high_phone = list(set(self.voc[["phone_no_m", "opposite_no_m"]][self.voc.apply(lambda x: True if x["phone_no_m"] in HighRiskOppositeNoM else False, axis=1)]["phone_no_m"].values))
            self.data["is_hit_rule_opposite"] = self.data.apply(lambda x: 1 if x["phone_no_m"] in high_phone else 0, axis=1)
        return self.data[["phone_no_m", column_name]]


    # 分箱特征
    def split_box_feature(self):
        print("--- 开始分箱的工作")

        if not self.is_train:
            self.data["arpu"] = self.data.apply(lambda x: float(0) if x["arpu"]=="\\N" else float(x["arpu"]), axis=1)

        # 单月消费太高
        self.data["high_arpu"] = self.data.apply(lambda x: 2 if x["arpu"] >= 520
            else (1 if x["arpu"] > 135 else 0), axis=1)

        # 绑定的身份证太多
        self.data["high_idcard_cnt"] = self.data.apply(lambda x: 2 if x["idcard_cnt"] > 7 else
            (1 if x["idcard_cnt"] > 2 else 0), axis=1)

        # 主呼记录中出现的用户太多
        self.data["high_initiative_voc_user_cnt"] = self.data.apply(
            lambda x: 2 if x["initiative_voc_user_cnt"] > 1275 else
            (1 if x["initiative_voc_user_cnt"] > 57 else 0), axis=1)

        # 通话记录一天中最大用户数太多
        self.data["high_voc_inner_day_user_cnt_max"] = self.data.apply(
            lambda x: 2 if x["voc_inner_day_user_cnt_max"] > 131 else
            (1 if x["voc_inner_day_user_cnt_max"] > 22 else 0), axis=1)

        # 通话记录一天中最小用户数过多
        self.data["high_voc_inner_day_user_cnt_min"] = self.data.apply(
            lambda x: 2 if x["voc_inner_day_user_cnt_min"] > 23 else
            (1 if x["voc_inner_day_user_cnt_min"] > 2 else 0), axis=1)

        # 用户一天内通话记录过多
        self.data["high_voc_inner_day_call_cnt_max"] = self.data.apply(
            lambda x: 1 if x["voc_inner_day_call_cnt_max"] > 41 else 0, axis=1)


    # 汇总所有特征的加工
    def init_features(self):
        text_to_print = "训练数据" if self.is_train else "测试数据"
        print("正在加工" + text_to_print + "特征")
        self.voc_user_cnt()
        self.initiative_voc_user_cnt()
        self.passive_voc_user_cnt()
        self.turn_voc_user_cnt()

        self.voc_user_call_cnt()
        self.initiative_voc_user_call_cnt()
        self.passive_voc_user_call_cnt()
        self.turn_voc_user_call_cnt()

        self.voc_inner_day_user_cnt()
        self.initiative_voc_inner_day_user_cnt()
        self.passive_voc_inner_day_user_cnt()
        self.turn_voc_inner_day_user_cnt()

        self.voc_inner_day_call_cnt()
        self.initiative_voc_inner_day_call_cnt()
        self.passive_voc_inner_day_call_cnt()
        self.turn_voc_inner_day_call_cnt()

        self.voc_call_cnt()
        self.initiative_voc_call_cnt()
        self.passive_voc_call_cnt()
        self.turn_voc_call_cnt()

        self.initiative_voc_ratio()
        self.passive_voc_ratio()
        self.turn_voc_ratio()

        self.sms_cnt()
        self.initiative_sms_cnt()
        self.passive_sms_cnt()

        self.sms_user_cnt()
        self.initiative_sms_user_cnt()
        self.passive_sms_user_cnt()

        self.initiative_sms_ratio()
        self.passive_sms_ratio()

        self.app_cnt()
        self.flow()

        self.voc_city_cnt()
        self.initiative_voc_city_cnt()
        self.passive_voc_city_cnt()
        self.turn_voc_city_cnt()

        self.voc_interval()
        self.initiative_voc_interval()
        self.passive_voc_interval()
        self.turn_voc_interval()

        self.voc_imei_cnt()
        self.initiative_voc_imei_cnt()
        self.passive_voc_imei_cnt()
        self.turn_voc_imei_cnt()

        self.voc_dur()
        self.initiative_voc_dur()
        self.passive_voc_dur()
        self.turn_voc_dur()

        self.initiative_voc_dur_ratio()
        self.passive_voc_dur_ratio()
        self.turn_voc_dur_ratio()

        self.voc_active_days()
        self.initiative_voc_active_days()
        self.passive_voc_active_days()
        self.turn_voc_active_days()

        self.sms_active_days()
        self.initiative_sms_active_days()
        self.passive_sms_active_days()

        self.voc_user_contact_days()
        self.initiative_voc_user_contact_days()
        self.passive_voc_user_contact_days()
        self.turn_voc_user_contact_days()

        self.call_activate_days_diff()
        self.sms_activate_days_diff()

        self.voc_inner_hour_cnt()
        self.initiative_voc_inner_hour_cnt()
        self.passive_voc_inner_hour_cnt()
        self.turn_voc_inner_hour_cnt()

        self.sms_inner_hour_cnt()
        self.initiative_sms_inner_hour_cnt()
        self.passive_sms_inner_hour_cnt()

        self.voc_inner_day_dur()
        self.initiative_voc_inner_day_dur()
        self.passive_voc_inner_day_dur()

        self.interactive_voc_user_cnt()
        self.interactive_sms_user_cnt()
        self.interactive_voc_user_ratio()
        self.interactive_sms_user_ratio()

        # self.split_box_feature()
        self.night_voc_ratio_too_high()
        self.has_we_chat()
        self.imei_cnt_about()
        self.frequency_initiative_voc()

        # 2020年8月13日添加
        self.has_app()
        self.last_call_is_before_24()
        self.has_too_many_id_card()
        self.passive_voc_avg_dur_too_low()
        self.has_county()
        self.initiative_voc_has_too_many_phone()

        self.is_hit_rule_app()
        self.is_hit_rule_opposite()
